import pytest
import os
import zipfile
from parser.apk_parser import APKParser

@pytest.fixture
def dummy_apk_path(tmp_path):
    apk_path = tmp_path / "dummy.apk"
    with zipfile.ZipFile(apk_path, 'w') as zf:
        zf.writestr("AndroidManifest.xml", b"dummy")
    return str(apk_path)

@pytest.fixture
def malformed_apk_path(tmp_path):
    apk_path = tmp_path / "malformed.apk"
    with open(apk_path, 'w') as f:
        f.write("not a zip file")
    return str(apk_path)

def test_load_nonexistent_file():
    parser = APKParser("does_not_exist.apk")
    with pytest.raises(FileNotFoundError):
        parser.load()

def test_load_malformed_file(malformed_apk_path):
    parser = APKParser(malformed_apk_path)
    with pytest.raises(Exception) as excinfo:
        parser.load()
    assert "ENVIRONMENT: Bad or malformed ZIP/APK file" in str(excinfo.value)

def test_load_valid_file():
    parser = APKParser("samples/app.apk")
    assert parser.load() is True
    assert parser.get_package_name() == "io.appium.android.apis"
    assert parser.get_component_counts()[0] > 0

def test_getters_without_load():
    parser = APKParser("does_not_exist.apk")
    assert parser.get_package_name() == "Unknown"
    assert parser.get_version() == ("Unknown", "Unknown")
    assert parser.get_sdk_versions() == ("Unknown", "Unknown")
    assert parser.get_permissions() == []
    assert parser.get_component_counts() == (0, 0, 0)
