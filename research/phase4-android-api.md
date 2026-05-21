# Phase 4 Research: Android API Compatibility Layer

## Android API Surface
Android apps primarily interact with the OS through the `android.*` and `java.*` namespaces. To run Android apps on Linux without an emulator or full Android framework container (like Waydroid), we must intercept calls to these APIs and translate them to Linux equivalents.

## Target Translations
*   **android.util.Log:** The Android logging system. Mapped to Python's built-in `logging` module, which could later be configured to dump to systemd's `journald` or standard output.
*   **android.content.Context:** The global context object in Android (used for accessing resources, databases, preferences). We will implement a `RuntimeContext` stub that provides mock application-level data.
*   **android.content.Intent:** Android's IPC mechanism for launching components. Translated into simple dbus signals or an internal Python message bus (`IntentSystem`) for Phase 4.
*   **android.os.Bundle:** A string-to-object mapping. Translated to a standard Python dictionary wrapper.
*   **android.os.Environment:** Maps Android standard directories (like external storage) to Linux XDG directories (e.g., `~/.local/share/ares/<pkg>/`).
*   **android.net:** Translated to Python's `socket` or `urllib`.

## APIRouter Interception Architecture
Instead of compiling a massive set of C++ JNI libraries up front, our Phase 4 architecture uses an `APIRouter`. When the Phase 3 opcode interpreter encounters an `invoke-*` instruction targeting an `android.*` API, it delegates execution to the `APIRouter`. The router maps the Java class and method signature to a Python stub implementation.

## Security and Permissions
Android enforces permissions (e.g., `INTERNET`) at runtime. We will build a `PermissionEnforcer` that checks the APK's requested permissions (extracted in Phase 1) before allowing an API stub (like network access) to execute.
