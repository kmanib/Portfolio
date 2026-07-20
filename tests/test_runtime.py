import pytest
from runtime.dalvik.dex_parser import DexParser
from runtime.dalvik.class_loader import StubClassLoader
from runtime.dalvik.opcode_interpreter import OpcodeInterpreter
from runtime.loader import RuntimeLoader

# Mock for Androguard structures
class MockInstruction:
    def __init__(self, name, output):
        self._name = name
        self._output = output
    def get_name(self): return self._name
    def get_output(self): return self._output

class MockCodeBC:
    def get_instructions(self):
        return [
            MockInstruction('add-int', 'v0, v1, v2'),
            MockInstruction('if-eq', 'v0, v1, +5'),
            MockInstruction('invoke-virtual', 'Ljava/lang/String;->length()I'),
            MockInstruction('return-void', '')
        ]

class MockCode:
    def get_bc(self): return MockCodeBC()

class MockMethod:
    def __init__(self, name):
        self._name = name
    def get_name(self): return self._name
    def get_code(self): return MockCode()

class MockClass:
    def __init__(self, name):
        self._name = name
    def get_name(self): return self._name
    def get_superclassname(self): return "Ljava/lang/Object;"
    def get_interfaces(self): return []
    def get_methods(self): return [MockMethod('testMethod')]
    def get_fields(self): return []

class MockDexParser(DexParser):
    def __init__(self):
        super().__init__("dummy.apk")
        self.classes = {"Lorg/example/Test;": MockClass("Lorg/example/Test;")}
    def load(self):
        pass # mock

def test_class_loader():
    parser = MockDexParser()
    loader = StubClassLoader(parser)
    c = loader.load_class("Lorg/example/Test;")

    assert c['name'] == "Lorg/example/Test;"
    assert "testMethod" in c['methods']

def test_opcode_interpreter():
    interpreter = OpcodeInterpreter()
    method = MockMethod("testMethod")
    trace = interpreter.interpret(method)

    assert len(trace) == 4
    assert "ARITHMETIC: add-int" in trace[0]
    assert "CONTROL_FLOW: if-eq" in trace[1]
    assert "INVOKE: invoke-virtual" in trace[2]
    assert "RETURN: return-void" in trace[3]

def test_runtime_loader(monkeypatch):
    monkeypatch.setattr("runtime.loader.DexParser", lambda p: MockDexParser())

    loader = RuntimeLoader("dummy.apk")
    loader.initialize()

    trace = loader.experimental_trace_method("Lorg/example/Test;", "testMethod")
    assert trace is not None
    assert len(trace) > 0
