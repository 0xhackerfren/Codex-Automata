"""Bounded command output; POSIX group cleanup is not sandbox isolation."""
import hashlib
import os
import queue
import signal
import subprocess
import threading
import time


DEFAULT_OUTPUT_LIMIT = 1048576
MAX_OUTPUT_LIMIT = 16777216


def run_check(argv, cwd, timeout, output_limit=DEFAULT_OUTPUT_LIMIT):
    if type(output_limit) is not int or not 1 <= output_limit <= MAX_OUTPUT_LIMIT:
        raise ValueError('Invalid command output limit')
    chunks = queue.Queue(maxsize=4)
    stopped = threading.Event()
    hasher = hashlib.sha256()
    size, excerpt, code, failure = 0, b'', None, None
    process = None
    reader = None
    deadline = time.monotonic() + timeout

    def stop_process():
        if process is None:
            return
        try:
            if os.name == 'posix':
                os.killpg(process.pid, signal.SIGKILL)
            elif process.poll() is None:
                process.kill()
        except ProcessLookupError:
            pass

    def read_output():
        try:
            with process.stdout:
                while not stopped.is_set():
                    data = os.read(process.stdout.fileno(), 65536)
                    while not stopped.is_set():
                        try:
                            chunks.put(data, timeout=0.02)
                            break
                        except queue.Full:
                            pass
                    if not data:
                        return
        except OSError as exc:
            while not stopped.is_set():
                try:
                    chunks.put(exc, timeout=0.02)
                    return
                except queue.Full:
                    pass

    try:
        process = subprocess.Popen(argv, cwd=cwd, stdin=subprocess.DEVNULL,
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                   shell=False, start_new_session=os.name == 'posix')
        reader = threading.Thread(target=read_output, daemon=True)
        reader.start()
        eof = False
        while True:
            code = process.poll()
            if code is not None:
                # Do not let descendants outlive a successful direct child or
                # hold its pipe open indefinitely. Buffered output still drains.
                stop_process()
                if eof:
                    break
            if time.monotonic() >= deadline:
                failure = 'timeout'
                break
            try:
                data = chunks.get(timeout=min(0.02, max(0.001, deadline - time.monotonic())))
            except queue.Empty:
                continue
            if isinstance(data, OSError):
                failure = type(data).__name__
                break
            if not data:
                eof = True
                continue
            retained = data[:output_limit - size]
            hasher.update(retained)
            size += len(retained)
            excerpt += retained[:max(0, 8192 - len(excerpt))]
            if len(retained) != len(data):
                failure = 'output-limit'
                break
    except OSError as exc:
        failure = type(exc).__name__
    finally:
        stopped.set()
        stop_process()
        if process is not None:
            process.wait()
        if reader is not None:
            # A detached descendant can retain a Windows pipe. A daemon reader
            # and bounded queue keep cleanup bounded; host isolation is required.
            reader.join(timeout=0.2)
    return dict(exit_code=code if failure is None else None, failure=failure,
                output_sha256=hasher.hexdigest(), output_bytes=size,
                output_excerpt=excerpt.decode('utf-8', errors='replace'))
