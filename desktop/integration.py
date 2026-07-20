import os
import io
import stat
from PIL import Image
import zipfile
import lxml.etree as etree

class DesktopIntegration:
    def __init__(self, apk_parser):
        self.apk_parser = apk_parser
        self.apk_path = apk_parser.apk_path
        self.package = apk_parser.get_package_name()

        # Determine XDG base directories (defaulting if not set)
        data_home = os.environ.get('XDG_DATA_HOME', os.path.expanduser('~/.local/share'))
        self.applications_dir = os.path.join(data_home, 'applications')
        self.icons_dir = os.path.join(data_home, 'icons', 'hicolor')

    def _extract_icon(self):
        """Attempts to extract the highest resolution icon from the APK."""
        if not self.apk_parser.apk:
            return None, None

        icon_path = self.apk_parser.apk.get_element("application", "icon")
        if not icon_path:
            return None

        # Often starts with @ref/0xsomething. We let androguard resolve it if possible.
        # But for reliability, we can search the APK's res folder.
        apk = self.apk_parser.apk
        zip_obj = zipfile.ZipFile(self.apk_path)

        best_icon_data = None
        best_size = 0

        # Search for mipmap/drawable that contains 'icon' or matches the resolved name
        for filename in zip_obj.namelist():
            if 'res/mipmap' in filename or 'res/drawable' in filename:
                if 'icon.png' in filename or 'ic_launcher.png' in filename:
                    try:
                        data = zip_obj.read(filename)
                        img = Image.open(io.BytesIO(data))
                        if img.size[0] > best_size:
                            best_size = img.size[0]
                            best_icon_data = data
                    except:
                        pass

        if best_icon_data:
            return best_icon_data, best_size

        return None, None

    def install_icon(self):
        """Extracts and installs the APK icon to XDG directories."""
        icon_data, size = self._extract_icon()
        if not icon_data:
            return False

        # Select best standard size
        std_sizes = [16, 24, 32, 48, 64, 128, 256, 512]
        target_size = min(std_sizes, key=lambda x: abs(x - size))

        target_dir = os.path.join(self.icons_dir, f"{target_size}x{target_size}", "apps")
        os.makedirs(target_dir, exist_ok=True)

        icon_path = os.path.join(target_dir, f"ares_{self.package}.png")
        with open(icon_path, 'wb') as f:
            f.write(icon_data)

        return f"ares_{self.package}"

    def get_app_name(self):
        if not self.apk_parser.apk:
            return self.package
        name = self.apk_parser.apk.get_app_name()
        if not name:
            name = self.package
        return name

    def generate_desktop_file(self):
        """Generates and installs a .desktop file for the APK."""
        icon_name = self.install_icon() or "applications-development"
        app_name = self.get_app_name()

        # Resolve path to our launcher script
        launcher_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "cli", "main.py" # Phase 2 uses cli/main.py. We will use a dedicated launcher later.
        )

        desktop_content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name={app_name}
Comment=Android APK ({self.package})
Exec=python3 {launcher_path} %f
Icon={icon_name}
Terminal=true
Categories=Development;
MimeType=application/vnd.android.package-archive;
"""

        os.makedirs(self.applications_dir, exist_ok=True)
        desktop_file_path = os.path.join(self.applications_dir, f"ares_{self.package}.desktop")

        with open(desktop_file_path, 'w') as f:
            f.write(desktop_content)

        # Make it executable
        st = os.stat(desktop_file_path)
        os.chmod(desktop_file_path, st.st_mode | stat.S_IEXEC)

        return desktop_file_path

    def register_mime_type(self):
        """Associates .apk files with our launcher."""
        mime_dir = os.path.join(os.environ.get('XDG_DATA_HOME', os.path.expanduser('~/.local/share')), 'mime', 'packages')
        os.makedirs(mime_dir, exist_ok=True)

        mime_content = """<?xml version="1.0" encoding="UTF-8"?>
<mime-info xmlns="http://www.freedesktop.org/standards/shared-mime-info">
  <mime-type type="application/vnd.android.package-archive">
    <comment>Android Package Archive</comment>
    <glob pattern="*.apk"/>
  </mime-type>
</mime-info>
"""
        mime_path = os.path.join(mime_dir, 'ares-apk.xml')
        with open(mime_path, 'w') as f:
            f.write(mime_content)

        try:
            import subprocess
            subprocess.run(['update-mime-database', os.path.dirname(mime_dir)], check=False)
            subprocess.run(['update-desktop-database', self.applications_dir], check=False)
        except:
            pass # Tools might not be available

        return mime_path
