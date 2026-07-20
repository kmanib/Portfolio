import argparse
import sys
import os

# Add root directory to python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parser.apk_parser import APKParser

def main():
    parser = argparse.ArgumentParser(description="APK Inspector Engine - Extract metadata from APK files.")
    parser.add_argument("apk_path", help="Path to the APK file to inspect.")
    args = parser.parse_args()

    apk_parser = APKParser(args.apk_path)

    try:
        apk_parser.load()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    package = apk_parser.get_package_name()
    version_name, version_code = apk_parser.get_version()
    min_sdk, target_sdk = apk_parser.get_sdk_versions()
    permissions = apk_parser.get_permissions()
    activities, services, receivers = apk_parser.get_component_counts()

    # Format the permissions
    if permissions:
        # Extract just the permission name from the full string if it starts with android.permission.
        formatted_perms = " \u00b7 ".join([p.split('.')[-1] for p in permissions])
    else:
        formatted_perms = "None"

    # Print structured output
    print("┌─ APK Inspector ─────────────────────────────────")
    print(f"│ Package    : {package}")
    print(f"│ Version    : {version_name} ({version_code})")
    print(f"│ Min SDK    : {min_sdk}  │  Target SDK : {target_sdk}")
    print(f"│ Permissions:")

    # Handle wrapping for long permission lists
    import textwrap
    wrapped_perms = textwrap.wrap(formatted_perms, width=44)
    for line in wrapped_perms:
        print(f"│   {line}")

    print(f"│ Components:")
    print(f"│   Activities : {activities}  │  Services : {services}  │  Receivers : {receivers}")
    print("└─────────────────────────────────────────────────")

if __name__ == "__main__":
    main()
