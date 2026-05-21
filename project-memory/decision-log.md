# decision-log

Created: Wed May 20 17:12:35 UTC 2026

## Phase 1 Decisions
* Used `androguard` as the APK parsing engine due to its robust support for AXML decoding and component extraction.
* Output formatted directly in CLI.
* Testing implemented using `pytest`.

## Phase 2 Decisions
* Used PyGObject (GTK4) for the desktop browser GUI due to native Linux integration and modern libadwaita styling.
* Used dbus-python for DBus stubs.
* Opted for direct zipfile manipulation alongside androguard to forcefully locate APK icons if standard AndroidManifest references fail or point to uncompilable resources.
