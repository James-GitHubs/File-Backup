import os
import hashlib
import shutil

# Define active folder to backup
folder_original = r"D:\Documents"

# Define location of backup folder
folder_backup = r"S:\Documents"

# Define array for checksums & locations of original files
file_original = []
check_original = []

# Define array for checksums & locations of backup files
file_backup = []
check_backup = []


# Generate Checksums of file
def generate_checksum(file_path):
    sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            for block in iter(lambda: f.read(4096), b''):
                sha256.update(block)
    except IOError:
        print(f"Could not read file: {file_path}")
        return None
    return sha256.hexdigest()


# Find all files in directory and send each file to generate_checksum
def process_directory(directory, folder_num):
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            # print(f"Processing file: {file_path}")  # Debug print
            checksum = generate_checksum(file_path)
            if checksum:
                # Define if using original or backup folder
                if folder_num == 0:
                    # Remove the folder location so that they can be compared
                    file_path = file_path.removeprefix(folder_original)
                    # Add file path and checksum together in string
                    file_original.append(file_path)
                    check_original.append(checksum)
                elif folder_num == 1:
                    # Remove the folder location so that they can be compared
                    file_path = file_path.removeprefix(folder_backup)
                    # Add file path and checksum together in string
                    file_backup.append(file_path)
                    check_backup.append(checksum)


def deal_with_old(file):
    # Currently deletes outdated backup files before copying new. Change this to do something else if you want.
    try:
        print("Deleting:", file)
        os.remove(file)
        return 0
    except PermissionError as e:
        print("Error when deleting old backup file:", e)
        return 1
    except Exception as e:
        print(e)
        return 1


def copy_file(item, item2):
    # Check if file exists in backup folder, though checksum wrong
    if os.path.isfile(folder_backup + item):
        deal_with_old(folder_backup + item)
        result = copy_file(item, item2)
        if result == 1:
            # Stop infinite loop if can't delete file
            print("Failed to delete", folder_backup + item)
            return 1
    else: # if file doesn't exist, do copy
        try:
            shutil.copy(folder_original + item, folder_backup + item)
            print("File Copied.")
            return 0
        except FileNotFoundError as e:
            print("Directory not found making:")
            directory = os.path.dirname(folder_backup + item)
            os.makedirs(directory, exist_ok=True)
            # Do it again
            copy_file(item, item2)
        except PermissionError as e:
            print(e)
        except Exception as e:
            print(e)


def main():
    if not os.path.exists(folder_original):
        print(f"Original folder does not exist: {folder_original}")
        return
    if not os.path.exists(folder_backup):
        print(f"Backup folder does not exist: {folder_backup}")
        return

    print("\nGenerating Checksum for", folder_original)
    process_directory(folder_original, 0)

    print("\nChecksum generation. Generating Checksum for:", folder_backup)
    process_directory(folder_backup, 1)

    for item, item2 in zip(file_original, check_original):
        try:
            # Check if file location and checksum matches backup folder
            if file_backup.index(item) is not None and check_backup.index(item2) is not None :
                pass
        except ValueError:
            print(item, item2, "Not Found. Copying.")
            result = copy_file(item, item2)
            if result == 0:
                print("Copied successfully.")
        except Exception as e:
            print(e)

    print("Backup Complete.")


if __name__ == '__main__':
    main()
