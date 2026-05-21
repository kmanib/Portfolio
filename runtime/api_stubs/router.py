from .log import AndroidLog
from .context import RuntimeContext
from .intent import Intent, IntentSystem
from .file import Environment
from .network import NetworkBridge

class PermissionEnforcer:
    def __init__(self, declared_permissions):
        self.declared_permissions = declared_permissions

    def check(self, permission):
        if permission not in self.declared_permissions:
            raise PermissionError(f"SecurityException: Permission {permission} was not requested in AndroidManifest.xml")
        return True

class APIRouter:
    def __init__(self, permissions):
        self.enforcer = PermissionEnforcer(permissions)
        self.intent_system = IntentSystem()
        self.trace_log = []

    def route_invoke(self, class_name, method_name, *args):
        """Intercepts Android API calls and routes them to Linux stubs."""
        self.trace_log.append(f"API CALL: {class_name}->{method_name}")

        # Routing logic
        if class_name == "Landroid/util/Log;":
            if method_name in ['d', 'i', 'w', 'e']:
                log_method = getattr(AndroidLog, method_name)
                return log_method(*args)

        elif class_name == "Landroid/content/Context;":
            # Just a placeholder routing for now
            pass

        elif class_name == "Landroid/os/Environment;":
            if method_name == "getExternalStorageDirectory":
                self.enforcer.check("android.permission.READ_EXTERNAL_STORAGE")
                return Environment.getExternalStorageDirectory()

        elif class_name == "Landroid/net/NetworkBridge;": # Simplified
            self.enforcer.check("android.permission.INTERNET")
            if method_name == "is_connected":
                return NetworkBridge.is_connected()

        # If API is not implemented, log and return None (safely stubbing it out)
        AndroidLog.w("APIRouter", f"Unimplemented API stub called: {class_name}->{method_name}")
        return None

    def get_api_trace(self):
        return self.trace_log
