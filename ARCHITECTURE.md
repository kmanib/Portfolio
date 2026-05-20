# ARCHITECTURE

## Phase 1: APK Inspector Engine

### Design Overview
Phase 1 focuses on extracting metadata from APK files without executing any code.

### Components
*   **parser/apk_parser.py:** Uses `androguard` to read the APK file, parse the `AndroidManifest.xml`, and extract required metadata such as package name, permissions, min/target SDK versions, and component counts (Activities, Services, Receivers).
*   **cli/main.py:** The entry point. It uses `argparse` to accept the path to an APK file and formats the output from `APKParser` into a clean, structured CLI output. It also implements graceful error handling for invalid or malformed APKs.
