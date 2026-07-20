# Phase 3 Research: Experimental Runtime Loader

## Dalvik Bytecode Format (DEX)
DEX (Dalvik Executable) is the format Android uses for compiled bytecode. It contains multiple sections:
- **Header:** Magic bytes (`dex\n035\0`), checksum, signature, file size, and offsets to other sections.
- **String IDs, Type IDs, Proto IDs, Field IDs, Method IDs:** Dictionaries mapping indices to actual strings, types, and signatures used across the bytecode.
- **Class Defs:** Information about each class (name, superclass, interfaces, source file, annotations, and class data like fields/methods offsets).
- **Data Section:** The actual bytecode instructions and structural data referenced by the arrays above.

## Android Runtime (ART)
Modern Android uses ART, which compiles DEX to native code (AOT/JIT) (`.oat` / `.vdex`). However, for the scope of our compatibility layer and experimental loader, interpreting the raw DEX bytecode directly (like early Dalvik) is a safe and robust first step before jumping to full JNI/Native AOT bridges (Phase 6).

## DEX Class Loading Pipeline
1. Load `classes.dex` from the APK.
2. Parse Class Defs to build a symbolic table of classes.
3. For each loaded class, extract methods and their associated `DalvikCode` (registers, instructions, try/catch blocks).
4. Resolve field and method cross-references symbolically.

## Smali / Opcodes
Dalvik is a register-based VM (unlike Java's stack-based VM). Opcodes are typically 1-3 bytes.
- Arithmetic: `add-int`, `sub-int`, etc.
- Control flow: `if-eq`, `goto`, `return`.
- Invocation: `invoke-virtual`, `invoke-direct`.

For Phase 3, we implement a safe execution trace for simple arithmetic and control flow opcodes.

## Python ctypes/cffi Bridge
Eventually, invoking native Android API libraries will require `ctypes` or `cffi`. For Phase 3, we simulate a sandboxed environment entirely in Python without hooking into system syscalls.
