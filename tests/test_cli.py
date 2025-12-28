import subprocess
import sys

def test_cli_runs():
    result = subprocess.run(
        [sys.executable, "validate.py", "dijamin berhasil"],
        capture_output=True,
        text=True
    )
    assert "Final Severity: HIGH" in result.stdout
