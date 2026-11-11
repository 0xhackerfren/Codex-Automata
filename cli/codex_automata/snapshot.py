"""Exact regular-blob snapshots and worktree content checks, not OS isolation."""
from contextlib import contextmanager
import hashlib
import os
from pathlib import Path
import subprocess
import tempfile

from .control import ControlError, require, safe_path


MAX_BLOB = 64 * 1024 * 1024
MAX_TREE = 256 * 1024 * 1024


def git_bytes(repo, *args):
    env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')
    try:
        return subprocess.check_output(['git', '-C', str(repo), *args], env=env,
                                       stderr=subprocess.DEVNULL, timeout=30)
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        raise ControlError('Cannot verify committed snapshot') from exc


def tree_entries(repo, head):
    entries = []
    for record in git_bytes(repo, 'ls-tree', '-r', '-z', head).split(b'\0'):
        if not record:
            continue
        metadata, raw_path = record.split(b'\t', 1)
        mode, kind, sha = metadata.decode('ascii').split()
        path = raw_path.decode('utf-8')
        safe_path(path)
        require(mode in ('100644', '100755') and kind == 'blob',
                'Snapshot requires regular files; symlinks/submodules need a reviewed adapter: ' + path)
        entries.append((mode, sha, path))
    return entries


def blob_sha(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def read_regular(root, path):
    root = Path(root).resolve()
    file = root / path
    require(file.resolve().is_relative_to(root) and file.is_file() and not file.is_symlink()
            and all(not p.is_symlink() for p in file.parents if p != root and root in p.parents),
            'Tracked file missing, symlinked or outside tree: ' + path)
    require(file.stat().st_size <= MAX_BLOB, 'Tracked blob exceeds snapshot size limit: ' + path)
    return file.read_bytes()


def verify_worktree(repo, head):
    # Index hints must not hide writes from Git status or phase gates.
    flags = git_bytes(repo, 'ls-files', '-v', '-z').split(b'\0')
    require(all(not r or (not chr(r[0]).islower() and r[:1] != b'S') for r in flags),
            'Hidden Git index flags (assume-unchanged/skip-worktree) are forbidden')
    entries = tree_entries(repo, head)
    autocrlf = subprocess.run(['git', '-C', str(repo), 'config', '--get', 'core.autocrlf'],
                             capture_output=True, text=True, timeout=30).stdout.strip().lower()
    total = 0
    for mode, sha, path in entries:
        data = read_regular(repo, path)
        require(os.name == 'nt' or bool((Path(repo) / path).stat().st_mode & 0o100) == (mode == '100755'),
                'Worktree executable mode differs from committed blob: ' + path)
        total += len(data)
        require(total <= MAX_TREE, 'Tracked tree exceeds snapshot size limit')
        if blob_sha(data) == sha:
            continue
        attrs = git_bytes(repo, 'check-attr', '-z', 'text', 'eol', 'filter', '--', path).split(b'\0')
        values = {attrs[i + 1].decode(): attrs[i + 2].decode() for i in range(0, len(attrs)-1, 3)}
        require(values.get('filter') in ('unspecified', 'unset'), 'Custom clean filters require a reviewed adapter: ' + path)
        text = values.get('text', 'unspecified')
        normalize = text != 'unset' and (text in ('set', 'auto') or values.get('eol') in ('lf', 'crlf')
                                       or autocrlf in ('true', 'input')) and b'\0' not in data[:8000]
        require(normalize and blob_sha(data.replace(b'\r\n', b'\n')) == sha,
                'Worktree content differs from committed blob: ' + path)
    return entries


@contextmanager
def committed_snapshot(repo, head, directory):
    entries = tree_entries(repo, head)
    with tempfile.TemporaryDirectory(prefix='automata-check-', dir=directory) as tmp:
        root = Path(tmp)
        # cat-file supplies raw object bytes: no export-ignore, export-subst,
        # smudge filters, local index hints or checkout line-ending conversions.
        process = subprocess.Popen(['git', '-C', str(repo), 'cat-file', '--batch'],
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                                   env=dict(os.environ, GIT_NO_REPLACE_OBJECTS='1'))
        total = 0
        try:
            for mode, sha, path in entries:
                process.stdin.write(sha.encode() + b'\n'); process.stdin.flush()
                header = process.stdout.readline().decode('ascii').strip().split()
                require(len(header) == 3 and header[:2] == [sha, 'blob'], 'Unexpected Git blob response')
                size = int(header[2]); total += size
                require(0 <= size <= MAX_BLOB and total <= MAX_TREE, 'Committed snapshot size limit exceeded')
                data = process.stdout.read(size)
                require(process.stdout.read(1) == b'\n' and blob_sha(data) == sha, 'Git blob integrity mismatch')
                destination = root / path
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(data)
                if mode == '100755':
                    destination.chmod(0o755)
            process.stdin.close()
            require(process.wait(timeout=30) == 0, 'Snapshot object reader failed')
            yield root, entries
        finally:
            if process.poll() is None:
                process.kill(); process.wait()
            if not process.stdin.closed:
                process.stdin.close()
            process.stdout.close()


def snapshot_unchanged(root, entries):
    try:
        return all(blob_sha(read_regular(root, path)) == sha
                   and (os.name == 'nt' or bool((Path(root) / path).stat().st_mode & 0o100) == (mode == '100755'))
                   for mode, sha, path in entries)
    except (ControlError, OSError):
        return False


def check_environment(root):
    allowed = ('PATH', 'PATHEXT', 'SYSTEMROOT', 'WINDIR', 'COMSPEC', 'TEMP', 'TMP', 'TMPDIR',
               'LANG', 'LC_ALL', 'LC_CTYPE')
    env = {k: v for k, v in os.environ.items() if k.upper() in allowed}
    env.update(HOME=str(root), USERPROFILE=str(root), PYTHONDONTWRITEBYTECODE='1')
    return env
