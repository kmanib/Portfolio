class OpcodeInterpreter:
    def __init__(self):
        self.trace_log = []

    def interpret(self, method):
        """
        Takes an Androguard EncodedMethod object.
        Interprets a safe subset of Dalvik opcodes (arithmetic, control flow).
        """
        code = method.get_code()
        if not code:
            self.trace_log.append(f"No code for {method.get_name()}")
            return []

        # Very basic symbolic interpreter loop
        # For Phase 3, we just parse the instruction format and log it.
        # We don't maintain a full register state yet to keep the sandbox strict.

        instructions = code.get_bc().get_instructions()

        for idx, inst in enumerate(instructions):
            op_name = inst.get_name()

            if 'add-int' in op_name or 'sub-int' in op_name:
                self.trace_log.append(f"[{idx}] ARITHMETIC: {op_name} {inst.get_output()}")
            elif op_name.startswith('if-') or op_name.startswith('goto'):
                self.trace_log.append(f"[{idx}] CONTROL_FLOW: {op_name} {inst.get_output()}")
            elif op_name.startswith('invoke-'):
                self.trace_log.append(f"[{idx}] INVOKE: {op_name} {inst.get_output()}")
            elif 'return' in op_name:
                self.trace_log.append(f"[{idx}] RETURN: {op_name} {inst.get_output()}")
            else:
                # Other opcodes are ignored in this phase
                pass

        return self.trace_log

    def get_trace(self):
        return self.trace_log
