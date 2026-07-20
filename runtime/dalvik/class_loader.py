class StubClassLoader:
    def __init__(self, dex_parser):
        self.dex_parser = dex_parser
        self.loaded_classes = {}

    def load_class(self, class_name):
        """Loads a class definition symbolically without executing it."""
        if class_name in self.loaded_classes:
            return self.loaded_classes[class_name]

        c = self.dex_parser.get_class(class_name)
        if not c:
            raise ImportError(f"Class not found in DEX: {class_name}")

        class_def = {
            'name': c.get_name(),
            'super': c.get_superclassname(),
            'interfaces': c.get_interfaces(),
            'methods': {},
            'fields': {}
        }

        for method in c.get_methods():
            class_def['methods'][method.get_name()] = method

        for field in c.get_fields():
            class_def['fields'][field.get_name()] = field

        self.loaded_classes[class_name] = class_def
        return class_def
