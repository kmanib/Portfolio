from androguard.core.bytecodes.apk import APK
import zipfile

class APKParser:
    def __init__(self, apk_path):
        self.apk_path = apk_path
        self.apk = None

    def load(self):
        try:
            self.apk = APK(self.apk_path)
            return True
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {self.apk_path}")
        except zipfile.BadZipFile:
            raise Exception("ENVIRONMENT: Bad or malformed ZIP/APK file")
        except Exception as e:
            raise Exception(f"PARSER: Failed to parse APK: {str(e)}")

    def get_package_name(self):
        if not self.apk:
            return "Unknown"
        return self.apk.get_package()

    def get_version(self):
        if not self.apk:
            return "Unknown", "Unknown"
        return self.apk.get_androidversion_name(), self.apk.get_androidversion_code()

    def get_sdk_versions(self):
        if not self.apk:
            return "Unknown", "Unknown"
        return self.apk.get_min_sdk_version(), self.apk.get_target_sdk_version()

    def get_permissions(self):
        if not self.apk:
            return []
        permissions = self.apk.get_permissions()
        # Deduplicate and sort
        return sorted(list(set(permissions)))

    def get_component_counts(self):
        if not self.apk:
            return 0, 0, 0
        activities = len(self.apk.get_activities())
        services = len(self.apk.get_services())
        receivers = len(self.apk.get_receivers())
        return activities, services, receivers
