import re

# Paths to files
init_file = "track_changes/__init__.py"
metadata_file = "track_changes/metadata.txt"

# Read version from __init__.py
with open(init_file, "r") as f:
  content = f.read()
  version_match = re.search(r'__version__\s*=\s*["\'](.+?)["\']', content)
  if not version_match:
    raise ValueError("Version not found in track_changes/__init__.py")
  version = version_match.group(1)

# Read metadata.txt
with open(metadata_file, "r") as f:
  metadata_content = f.read()

# Function to replace version correctly
def replace_version(match):
  return f"{match.group(1)}{version}"

# Perform substitution
new_metadata_content = re.sub(r"(version=)(.+)", replace_version, metadata_content)

# Write updated content back to metadata.txt
with open(metadata_file, "w") as f:
  f.write(new_metadata_content)

print(f"Updated metadata.txt to version {version}")