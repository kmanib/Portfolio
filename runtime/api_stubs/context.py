class RuntimeContext:
    def __init__(self, package_name):
        self.package_name = package_name
        self.resources = {}

    def getPackageName(self):
        return self.package_name

    def getString(self, res_id):
        return self.resources.get(res_id, f"res_0x{res_id:x}")

    def getSystemService(self, name):
        # Stub for returning system services
        return f"StubService_{name}"
