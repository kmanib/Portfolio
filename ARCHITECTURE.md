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
