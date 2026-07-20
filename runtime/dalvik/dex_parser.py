import os
from androguard.core.bytecodes import dvm

class DexParser:
    def __init__(self, apk_path):
        self.apk_path = apk_path
        self.dex_objects = []
        self.classes = {}

    def load(self):
        """Extracts and parses all classes.dex files from the APK."""
        import zipfile

        try:
            with zipfile.ZipFile(self.apk_path, 'r') as zf:
                dex_files = [name for name in zf.namelist() if name.startswith('classes') and name.endswith('.dex')]

                for dex_name in dex_files:
                    dex_data = zf.read(dex_name)
                    # Use androguard's DalvikVMFormat to parse the DEX data
                    d = dvm.DalvikVMFormat(dex_data)
                    self.dex_objects.append(d)

                    for c in d.get_classes():
                        self.classes[c.get_name()] = c

        except Exception as e:
            raise Exception(f"RUNTIME: Failed to parse DEX files: {str(e)}")

    def get_class_names(self):
        return list(self.classes.keys())

    def get_class(self, name):
        return self.classes.get(name)

    def get_methods_for_class(self, class_name):
        c = self.get_class(class_name)
        if not c:
            return []
        return c.get_methods()

    def get_fields_for_class(self, class_name):
        c = self.get_class(class_name)
        if not c:
            return []
        return c.get_fields()
