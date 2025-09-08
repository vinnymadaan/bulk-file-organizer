import argparse
import pathlib
import sys

FILE_TYPE_MAP = {
    "Images": ['.jpeg', '.jpg', '.png', '.gif', '.svg'],
    "Documents": ['.pdf', '.docx', '.txt', '.pptx', '.xlsx'],
    "Audio": ['.mp3', '.wav', '.aac'],
    "Video": ['.mp4', '.mov', '.avi', '.akv'],
    "Archives": ['.zip', '.rar', '.tar', '.gz'],
    "Other": []
}

def organize_directory(source_path: pathlib.Path):
    """
    Scans a directory and organizes files into subdirectories based on their type.

    This function is the main workhouse of the script. It will contain the logic
    for iterating through files, determining their type, creating destination
    folders, and moving the files.

    Args:
        source_path (pathlib.Path): The Path object representing the directory
                                    to be organized.
    """
    print(f"Organizing files in: {source_path}") 

    for item in source_path.iterdir():
        if item.is_file():
            file_extension = item.suffix.lower()
            print(f" - Found file: {item.name}, Extension: {file_extension}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Organize files in a directory by their type.")
    parser.add_argument("source_directory", help="The path to the directory you want to oragnize.")
    args = parser.parse_args()

    source_path = pathlib.Path(args.source_directory)

    if not source_path.exists() or not source_path.is_dir():
        print(f"Error: The path '{source_path}' does not exist or is not a directory.")
        sys.exit(1)
    organize_directory(source_path)
    