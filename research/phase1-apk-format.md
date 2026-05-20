# Phase 1 Research: APK Format and AndroidManifest.xml

## APK Structure
An APK (Android Package) file is essentially a ZIP archive containing the application's compiled code, resources, assets, certificates, and manifest file.

## AndroidManifest.xml Binary Format
The `AndroidManifest.xml` inside an APK is not a plain-text XML file. It is compiled into a binary XML format (AXML). This format is designed for size efficiency and fast parsing by the Android OS.

### Structure of Binary XML
*   **Header:** Contains magic number and file size.
*   **String Pool:** Contains all the strings used in the manifest (element names, attribute names, attribute values, etc.).
*   **Resource Map:** Maps resource IDs to strings.
*   **XML Tree:** A hierarchical representation of the XML document, where nodes reference strings from the string pool.

### Extracting Information
To read the binary XML, we can use libraries like `androguard`, which knows how to decode the AXML format and provide an object model representing the manifest's contents.

### Target Data
*   **Package Name:** Root `<manifest>` element `package` attribute.
*   **Version Info:** `android:versionCode` and `android:versionName` in the `<manifest>` element.
*   **SDK Info:** `<uses-sdk>` element `android:minSdkVersion` and `android:targetSdkVersion` attributes.
*   **Permissions:** `<uses-permission>` elements `android:name` attributes.
*   **Components:** `android:name` in `<activity>`, `<service>`, and `<receiver>` elements inside `<application>`.
