# ROADMAP

## Phase 1: APK Inspector Engine
Build a stable, reliable CLI tool for APK inspection and metadata extraction.
*   APK file loading and validation.
*   AndroidManifest.xml parsing.
*   Extraction of package name, permissions, version information, and components.

## Phase 2: Desktop Integration Layer
Make inspected APKs visible and launchable as Linux desktop applications.
*   Extract APK icon and generate `.desktop` file.
*   Install `.desktop` file and icon.
*   Register APK with XDG desktop environment.

## Phase 3: Experimental Runtime Loader
Begin loading and interpreting APK bytecode experimentally.
*   DEX file parser and basic opcode interpreter.
*   Stub classloader and execution trace logger.

## Phase 4: Android API Compatibility Layer
Translate core Android API calls into Linux equivalents.
*   Implement `runtime/api_stubs/` for core Android APIs (`Log`, `Context`, `Intent`, etc.).

## Phase 5: Graphics Translation Layer
Translate Android graphics APIs into Linux rendering equivalents.
*   OpenGL ES -> Mesa routing.
*   `Canvas`/`Bitmap` -> Cairo.
*   Android `View` -> GTK4 widget host.

## Phase 6: Native Linux APK Integration
Full native-grade APK execution on Linux.
*   Rewrite core runtime in Rust or C++.
*   ARM64 -> x86_64 translation.
*   Binder IPC -> dbus translation.
*   APK process sandboxing.
