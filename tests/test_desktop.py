import pytest
import os
import stat
from desktop.integration import DesktopIntegration
from desktop.launcher import DesktopLauncher
from parser.apk_parser import APKParser

@pytest.fixture
def dummy_apk_parser(tmp_path):
    apk_path = tmp_path / "dummy.apk"
    import zipfile
    with zipfile.ZipFile(apk_path, 'w') as zf:
        zf.writestr("AndroidManifest.xml", b"dummy")

    # Mock APKParser to not actually parse AXML, just hold the path and return dummy data
    class MockAPKParser:
        def __init__(self):
            self.apk_path = str(apk_path)
            self.apk = None
        def get_package_name(self):
            return "org.example.dummy"

    return MockAPKParser()

def test_generate_desktop_file(dummy_apk_parser, tmp_path, monkeypatch):
    integration = DesktopIntegration(dummy_apk_parser)

    # Redirect XDG directories to tmp_path for testing
    monkeypatch.setenv('XDG_DATA_HOME', str(tmp_path))
    integration.applications_dir = os.path.join(str(tmp_path), 'applications')
    integration.icons_dir = os.path.join(str(tmp_path), 'icons', 'hicolor')

    desktop_file = integration.generate_desktop_file()

    assert os.path.exists(desktop_file)
    with open(desktop_file, 'r') as f:
        content = f.read()
        assert "Name=org.example.dummy" in content
        assert "Exec=python3" in content

    # Check if executable
    st = os.stat(desktop_file)
    assert st.st_mode & stat.S_IEXEC

def test_generate_shell_launcher(tmp_path):
    launcher = DesktopLauncher("/fake/path/app.apk", "org.example.test")
    script_path = launcher.generate_shell_launcher(str(tmp_path))

    assert os.path.exists(script_path)
    with open(script_path, 'r') as f:
        content = f.read()
        assert "ARES Launcher Script for org.example.test" in content
        assert "/fake/path/app.apk" in content

    # Check if executable
    st = os.stat(script_path)
    assert st.st_mode & stat.S_IEXEC
