import zipfile
import os

def convert_metadata_to_utf8(metadata_file):
    """Ensure metadata.txt is UTF-8 encoded"""
    try:
        with open(metadata_file, "r", encoding="ISO-8859-1") as f:
            content = f.read()
        with open(metadata_file, "w", encoding="utf-8") as f:
            f.write(content)
        print("✔ metadata.txt converted to UTF-8")
    except Exception as e:
        print(f"⚠ Error converting metadata.txt: {e}")

def zip_qgis_plugin(plugin_folder, output_zip):
    """Zip the QGIS plugin, ensuring correct structure"""
    metadata_file = os.path.join(plugin_folder, "metadata.txt")
    
    if os.path.exists(metadata_file):
        convert_metadata_to_utf8(metadata_file)
    else:
        print("⚠ Warning: metadata.txt not found!")

    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(plugin_folder):
            dirs[:] = [d for d in dirs if d != "__pycache__"]
            for file in files:
                if not file.endswith(".pyc"):
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, os.path.dirname(plugin_folder))  # Ensure root folder
                    zipf.write(file_path, arcname)

    print(f"✔ QGIS plugin '{output_zip}' has been successfully created!")

plugin_name = "track_changes"
zip_qgis_plugin(plugin_name, f"{plugin_name}.zip")