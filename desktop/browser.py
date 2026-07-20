import gi
import sys
import os

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gio, GLib

class APKBrowserWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_default_size(600, 400)
        self.set_title("ARES APK Browser")

        # Main layout
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        vbox.set_margin_top(10)
        vbox.set_margin_bottom(10)
        vbox.set_margin_start(10)
        vbox.set_margin_end(10)
        self.set_child(vbox)

        # Header
        header = Gtk.Label()
        header.set_markup("<b>Installed APKs</b>")
        vbox.append(header)

        # Scrolled window for list
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        vbox.append(scrolled)

        # List Box
        self.listbox = Gtk.ListBox()
        self.listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        scrolled.set_child(self.listbox)

        self.populate_list()

    def populate_list(self):
        """Scans ~/.local/share/applications for ares_*.desktop files."""
        data_home = os.environ.get('XDG_DATA_HOME', os.path.expanduser('~/.local/share'))
        apps_dir = os.path.join(data_home, 'applications')

        if not os.path.exists(apps_dir):
            return

        for filename in os.listdir(apps_dir):
            if filename.startswith("ares_") and filename.endswith(".desktop"):
                filepath = os.path.join(apps_dir, filename)
                self.add_apk_row(filepath)

    def add_apk_row(self, desktop_path):
        # Extremely basic parser for the .desktop file
        name = "Unknown"
        package = "Unknown"
        with open(desktop_path, 'r') as f:
            for line in f:
                if line.startswith("Name="):
                    name = line.split("=")[1].strip()
                elif line.startswith("Comment="):
                    comment = line.split("=")[1].strip()
                    if "(" in comment and ")" in comment:
                        package = comment.split("(")[1].split(")")[0]

        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        row.set_margin_top(5)
        row.set_margin_bottom(5)

        icon = Gtk.Image.new_from_icon_name("application-x-executable")
        icon.set_pixel_size(48)
        row.append(icon)

        text_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        name_label = Gtk.Label()
        name_label.set_markup(f"<b>{name}</b>")
        name_label.set_halign(Gtk.Align.START)
        text_box.append(name_label)

        pkg_label = Gtk.Label(label=package)
        pkg_label.set_halign(Gtk.Align.START)
        text_box.append(pkg_label)

        row.append(text_box)

        # Add to listbox
        listbox_row = Gtk.ListBoxRow()
        listbox_row.set_child(row)
        self.listbox.append(listbox_row)

class APKBrowserApplication(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="org.ares.apkbrowser", flags=Gio.ApplicationFlags.FLAGS_NONE)

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = APKBrowserWindow(application=self)
        win.present()

def main():
    app = APKBrowserApplication()
    return app.run(sys.argv)

if __name__ == '__main__':
    sys.exit(main())
