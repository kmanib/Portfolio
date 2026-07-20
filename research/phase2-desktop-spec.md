# Phase 2 Research: Desktop Integration Layer

## XDG .desktop Specification
The XDG Desktop Entry Specification defines standard files for application launchers. These `.desktop` files are typically stored in `~/.local/share/applications/` for user-specific apps.
Key keys for APK integration:
- `Type=Application`
- `Name`: Extracted from APK Manifest (if available, or package name).
- `Icon`: The name of the icon file installed in `~/.local/share/icons/hicolor/...`.
- `Exec`: The command to launch the APK (e.g., a wrapper shell script or our launcher CLI).
- `Terminal=false`
- `MimeType=application/vnd.android.package-archive;` (for associating `.apk` files with our inspector).

## Icon Theme Specification
Icons should be placed in `~/.local/share/icons/hicolor/<size>x<size>/apps/`. APKs store icons in `res/drawable-*` or `res/mipmap-*` (hdpi, xhdpi, xxhdpi, etc.). We will extract these using `androguard` or `zipfile` and copy them to the appropriate XDG directories.

## DBus Integration
DBus is the IPC mechanism on Linux desktop. We will need DBus integration to handle launch events or signal the desktop environment about new applications. `dbus-python` is the standard library.

## GTK4 / libadwaita
For the simple APK browser GUI, GTK4 via PyGObject (`gi.repository.Gtk`) provides a native Linux look and feel. `libadwaita` adds GNOME integration (optional but nice).
We will build a simple `Gtk.Application` that lists installed APKs (which are essentially the `.desktop` entries or a local cache) and displays their metadata.

## xdg-open Compatibility
`xdg-open` is used to open files in their default application. Our launcher should handle `.apk` files by default and provide a compatibility stub for opening URLs or other files requested by the APK.
