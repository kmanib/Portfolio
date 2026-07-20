# ARCHITECTURE

## Phase 1: APK Inspector Engine

### Design Overview
Phase 1 focuses on extracting metadata from APK files without executing any code.

### Components
*   **parser/apk_parser.py:** Uses `androguard` to read the APK file, parse the `AndroidManifest.xml`, and extract required metadata such as package name, permissions, min/target SDK versions, and component counts (Activities, Services, Receivers).
*   **cli/main.py:** The entry point. It uses `argparse` to accept the path to an APK file and formats the output from `APKParser` into a clean, structured CLI output. It also implements graceful error handling for invalid or malformed APKs.

## Phase 2: Desktop Integration Layer

### Design Overview
Phase 2 enables the parsed APK to be integrated into the Linux desktop environment by extracting icons and generating standard XDG desktop launchers, as well as providing a simple GTK4 GUI to browse them.

### Components
*   **desktop/integration.py:** Handles parsing the APK icon via the `APKParser`, selecting the best resolution, installing it to the appropriate `~/.local/share/icons/hicolor/` directory, and generating a `.desktop` file in `~/.local/share/applications/` compliant with the XDG spec. It also registers MIME types for `.apk` files.
*   **desktop/launcher.py:** Generates a lightweight shell script wrap around the `cli/main.py` entrypoint. Features placeholder stubs for DBus signals and `xdg-open` which will be fleshed out in subsequent phases.
*   **desktop/browser.py:** A standalone GTK4 application (via `PyGObject`) that parses the generated `.desktop` files in `~/.local/share/applications/` and presents a simple GUI list of installed APKs along with their basic metadata.

## Phase 3: Experimental Runtime Loader

### Design Overview
Phase 3 focuses on parsing the Dalvik Executable (DEX) bytecode and providing a foundational, sandboxed interpreter for opcodes, without actual execution of system calls or deep Dalvik logic.

### Components
*   **runtime/dalvik/dex_parser.py:** Uses `androguard.core.bytecodes.dvm` to extract and parse the internal `classes.dex` elements into an object model representing classes, methods, and fields.
*   **runtime/dalvik/class_loader.py:** Implements a symbolic class loader (`StubClassLoader`) that manages a dictionary of parsed class definitions without executing `<clinit>` or instantiating objects.
*   **runtime/dalvik/opcode_interpreter.py:** A basic symbolic interpreter that parses Android's smali-like instruction objects and produces a safe execution trace for basic opcodes (arithmetic, control flow, invocation).
*   **runtime/loader.py:** Orchestrates the initialization of the DEX parser, the class loader, and the opcode interpreter to perform safe runtime tracing.

## Phase 4: Android API Compatibility Layer

### Design Overview
Phase 4 provides a simulated Android API surface allowing the interpreted Dalvik opcodes to interact with Linux OS equivalents without requiring Google Play Services or full Android framework containers.

### Components
*   **runtime/api_stubs/router.py:** The core `APIRouter` intercepts Android framework API calls (e.g., `invoke-*`) and maps them to Python equivalents. It also houses the `PermissionEnforcer`, which strictly validates the calling APK's declared permissions against the invoked stub.
*   **runtime/api_stubs/log.py:** Maps `android.util.Log` to the standard Python `logging` module.
*   **runtime/api_stubs/file.py:** Translates `android.os.Environment` requests (like `getExternalStorageDirectory`) to appropriate Linux `XDG` base directories, ensuring a sandboxed, desktop-compliant file system layout.
*   **runtime/api_stubs/network.py:** Implements basic networking stubs (`is_connected`, `simple_get`) using Python's `socket` and `urllib`.
*   **runtime/api_stubs/intent.py:** Provides a simplified `Intent` object model and a basic `IntentSystem` mock for broadcasting.
