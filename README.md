# File Backup Script

This Python script backs up all files from an original folder to a backup folder by comparing checksums. It ensures that any new or modified files in the original folder are copied to the backup folder, overwriting old files if necessary, while leaving any extra files in the backup folder alone.

## Features

- Backs up files from the original folder to the backup folder.
- Compares checksums of all files in the original folder against the backup folder.
- Copies files from the original folder to the backup folder if they do not exist or are different.
- Leaves any extra backup files alone.

## Requirements

- Python 3.x
- `hashlib` module (included in Python standard library)
- `shutil` module (included in Python standard library)
- `os` module (included in Python standard library)

## Usage

1. Set the path of the original folder and backup folder in the script:
   ```python
   folder_original = r"D:\Documents"
   folder_backup = r"S:\Documents"
