import pytest
import os
from runtime.api_stubs.router import APIRouter
from runtime.api_stubs.log import AndroidLog
from runtime.api_stubs.intent import Intent

def test_permission_enforcer():
    # Only granting INTERNET
    router = APIRouter(["android.permission.INTERNET"])

    # Should pass
    assert router.route_invoke("Landroid/net/NetworkBridge;", "is_connected") in [True, False]

    # Should fail (SecurityException)
    with pytest.raises(PermissionError) as exc:
        router.route_invoke("Landroid/os/Environment;", "getExternalStorageDirectory")
    assert "android.permission.READ_EXTERNAL_STORAGE" in str(exc.value)

def test_api_routing_log(capsys):
    router = APIRouter([])
    # The Log bridge doesn't currently check permissions
    router.route_invoke("Landroid/util/Log;", "i", "TestTag", "Test message")

    # We can check the router trace log
    trace = router.get_api_trace()
    assert "API CALL: Landroid/util/Log;->i" in trace

def test_intent_system():
    intent = Intent("android.intent.action.VIEW", "http://example.com")
    intent.putExtra("key", "value")

    assert intent.getExtra("key") == "value"
    assert intent.action == "android.intent.action.VIEW"
