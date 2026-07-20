import pytest
import subprocess
import os

def test_cli_help():
    result = subprocess.run(["python", "cli/main.py", "-h"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "APK Inspector Engine" in result.stdout

def test_cli_nonexistent_file():
    result = subprocess.run(["python", "cli/main.py", "does_not_exist.apk"], capture_output=True, text=True)
    assert result.returncode == 1
    assert "Error: File not found" in result.stdout

def test_cli_malformed_file(tmp_path):
    apk_path = tmp_path / "malformed.apk"
    with open(apk_path, 'w') as f:
        f.write("not a zip file")

    result = subprocess.run(["python", "cli/main.py", str(apk_path)], capture_output=True, text=True)
    assert result.returncode == 1
    assert "Error: ENVIRONMENT: Bad or malformed ZIP/APK file" in result.stdout

def test_cli_valid_file():
    result = subprocess.run(["python", "cli/main.py", "samples/app.apk"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "Package    : io.appium.android.apis" in result.stdout
    assert "Components:" in result.stdout
