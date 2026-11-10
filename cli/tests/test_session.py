from pathlib import Path
import subprocess
import tempfile
import unittest
from codex_automata.session import inspect_surface


class SessionTests(unittest.TestCase):
    def test_local_only_and_actual_remote_publication_observation(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / 'repo'
            remote = Path(tmp) / 'remote.git'
            repo.mkdir()
            def git(*args):
                return subprocess.check_output(['git','-C',str(repo),*args], stderr=subprocess.DEVNULL)
            git('init','-b','main')
            git('config','user.name','Fixture')
            git('config','user.email','fixture@example.invalid')
            (repo/'spec.md').write_text('spec')
            git('add','.')
            git('commit','-m','baseline')
            self.assertTrue(inspect_surface(repo)['valid'])
            self.assertFalse(inspect_surface(repo, True)['valid'])
            subprocess.check_output(['git','init','--bare',str(remote)],stderr=subprocess.DEVNULL)
            git('remote','add','origin',str(remote))
            self.assertFalse(inspect_surface(repo,True)['valid'])
            git('push','origin','main')
            self.assertTrue(inspect_surface(repo,True)['last_pushed_head_matches'])
            (repo/'spec.md').write_text('changed')
            git('add','.')
            git('commit','-m','unpublished')
            self.assertEqual(inspect_surface(repo,True)['publication_state'],'pending-publication')
