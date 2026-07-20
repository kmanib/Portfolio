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

## Phase 3 Decisions
* Used Androguard's `DalvikVMFormat` rather than writing a raw DEX parser from scratch to save time and leverage stable parsing of string pools and field offsets.
* Kept the opcode interpreter strictly symbolic (producing a trace log rather than executing native CPU instructions or maintaining simulated register state) to adhere to the "safe sandbox" requirement.

## Phase 4 Decisions
* Used a dynamic routing dictionary (`APIRouter`) to map Java string signatures to Python static methods rather than attempting full JNI translation at this stage. This keeps the implementation Python-native and highly maintainable for the compatibility layer.
* Enforced Android manifest permissions natively at the point of API routing. If the app didn't declare it in the `APKParser` phase, the `PermissionEnforcer` immediately throws a `SecurityException` variant.
