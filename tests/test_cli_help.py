import subprocess
import sys


def test_cli_runs_and_can_find_assets():
    r = subprocess.run(
        [sys.executable, "-m", "im_python", "--help"], capture_output=True
    )
    assert r.returncode == 0
