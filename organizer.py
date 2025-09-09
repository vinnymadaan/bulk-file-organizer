import argparse
import pathlib
import sys
import shutil
import logging
import json

from tqdm import tqdm

FILE_TYPE_MAP = {
    "Images": ['.jpeg', '.jpg', '.png', '.gif', '.svg'],
    "Documents": ['.pdf', '.docx', '.txt', '.pptx', '.xlsx'],
    "Audio": ['.mp3', '.wav', '.aac'],
    "Video": ['.mp4', '.mov', '.avi', '.akv'],
    "Archives": ['.zip', '.rar', '.tar', '.gz'],
    "Other": []
}

def organize_directory(source_path: pathlib.Path, dry_run: bool):
    """
    Scans a directory and organizes files into subdirectories based on their type.
    Now includes a dry_run mode to simulate the organization.

    Args:
        source_path (pathlib.Path): The directory to be organized.
        dr_run (bool): if True, simulate the without moving files.
    """
    logging.info(f"Starting to organize directory: {source_path}")

    if dry_run:
        logging.info("--- DRY RUN MODE ENABLED: No files will be moved. ---")

    else:
        logging.warning("--- LIVE RUN MODE ENABLED: File system changes will be made. ---")


    files_to_process = [item for item in source_path.iterdir() if item.is_file()]

    for item in tqdm(files_to_process, desc="Organizing Files"):
        file_extension = item.suffix

    file_extension = item.suffix.lower()

    destination_folder_name = "Other"
    for category, extensions in FILE_TYPE_MAP.items():
        if file_extension in extensions:
            destination_folder_name = category
            break

    destination_dir = source_path / destination_folder_name

    if dry_run :
        destination_file_path = destination_dir / item.name
        logging.info(f"[DRY RUN] Would move '{item.name}' -> '{destination_file_path}'")
    else:

        destination_dir.mkdir(parents=True, exist_ok=True)

        destination_file_path = destination_dir / item.name

    counter = 1

    while destination_file_path.exists():
        logging.warning(f"Conflict: '{destination_file_path}' already exists.")
        new_filename = f"{item.stem} ({counter}){item.suffix}"
        destination_file_path = destination_dir / new_filename
        counter += 1

    try:
        shutil.move(item, destination_file_path)

        logging.info(f"Moved: '{item.name}' -> {destination_file_path}")
    except PermissionError as e:
        logging.error(f"Could not move '{item.name}'. Error: {e}" )

    except Exception as e:
        logging.error(f"An unexpected error occured while moving '{item.name}'. error: {e}")
        pass
    shutil.move(item, destination_file_path)
    print(f"Moved: '{item.name}' -> '{destination_file_path}'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Organize files in a directory by their type.")
    parser.add_argument("source_directory", help="The path to the directory you want to oragnize.")
    parser.add_argument('--dry-run', action='store_true', help='Stimulate the organization without moving files.')
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers = [
            logging.FileHandler("organizer.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    source_path = pathlib.Path(args.source_directory)

    if not source_path.is_dir():
        logging.error(f"Error: The provided path '{source_path}' is not valid directory.")
        sys.exit(1)
    organize_directory(source_path,  args.dry_run)
    