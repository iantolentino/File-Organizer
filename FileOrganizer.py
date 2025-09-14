#!/usr/bin/env python3
"""
File Organizer Script
---------------------
Organize files in a target directory into a categorize subfolders
(ee.g., Images, Documents, Videos) based on file extensions.

Features:
    - Clean architecture using FileOrganizer class
    - Extensible category system via FILE_CATEGORIES
    - Robust duplicate filename handling
    - Logging system for transparency and debugging
    - Modern Practices: pathlib, type hints, argparse
    - Optional --watch mode to auto-organize nwew files in real time
    
Author: Ian Tolentino
Date: 09/14/25
"""

import shutil
import logging
import argparse
import time
from pathlib import Path
from typing import Dict, List
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# CONFIGURATION

FILE_CATEGORIES: Dict[str, List[str]]= {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".csv"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv", ".flv", ".wmv"],
    "Audio": [".mp3", ".wav", ".aac", ".flac", ".ogg"],
    "Archives": [".zip", ".rar", ".tar", ".gz", ".7z"],
    "Scripts": [".py", ".js", ".sh", ".bat", ".rb", ".php"],
    "Others": []  # Fallback category
}

LOG_FILE =  "file_organizer.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# CORE CLASS
class FileOrganizer:
    """
    Class responsible for organizing files into categorized folders.
    """

    def __init__(self, base_path: Path):
        self.base_path = base_path

    def create_category_folders(self) -> None:
        """Ensure all category folders exist inside the base directory."""
        for category in FILE_CATEGORIES.keys():
            folder_path = self.base_path / category
            folder_path.mkdir(exist_ok=True)
            logging.debug(f"Ensured folder exists: {folder_path}")

    def get_file_category(self, file_extension: str) -> str:
        """
        Determine the category of a file based on its extension.
        Falls back to 'Others' if not matched.
        """
        for category, extensions in FILE_CATEGORIES.items():
            if file_extension.lower() in extensions:
                return category
        return "Others"
    
    def resolve_duplicate(self, destination: Path) -> Path:
        """
        Handle duplicate filenames by appending a counter befor the extension.
        Example: file.txt -> file(1).txt
        """
        counter = 1
        new_destination = destination
        while new_destination.exists():
            new_name = f"{destination.stem}({counter}){destination.suffix}"
            new_destination = destination.with_name(new_name)
            counter += 1
        return new_destination
    
    def move_file(self, file_path: Path, destination_dir: Path) -> None: 
        """
        Move a file to its destination directory
        Handles duplicates gracefully and logs the operation.
        """
        try:
            destination = destination_dir / file_path.name
            destination = self.resolve_duplicate(destination)
            shutil.move(str(file_path), str(destination))
            logging.info(f"Moved: {file_path} -> {destination}")
        except Exception as e:
            logging.error(f"Failed to move {file_path}: {e}")
    
    def organize_files(self) -> None:
        """
        Organize all files in the base directory into categorized folders.
        """
        logging.info(f"Starting orgranization in: {self.base_path}")
        self.create_category_folders()
        
        for item in self.base_path.iterdir():
            if item.is_file():
                category = self.get_file_category(item.suffix)
                destination_dir = self.base_path / category
                self.move_file(item, destination_dir)

        logging.info("File organization complete")

# Watch mode / Auto Mode Configurations
class WatchdogHandler(FileSystemEventHandler):
    """
    Watches a directory for new files and organizes them automatically.
    """

    def __init__(self, organizer: FileOrganizer):
        super().__init__()
        self.organizer = organizer
    
    def on_created(self, event):
        """Triggered when a new file is created."""
        if not event.is_directory:
            file_path = Path(event.src_path)
            category = self.organizer.get_file_category(file_path.suffix)
            destination_dir = self.organizer.base_path / category
            self.organizer.move_file(file_path, destination_dir)

def watch_directory(organizer: FileOrganizer) -> None:
    """
    Continuously watch the directory for new files and auto-organize them.
    """
    event_handler = WatchdogHandler(organizer)
    observer = Observer()
    observer.schedule(event_handler, str(organizer.base_path), recursive=False)
    observer.start()

    logging.info(f"Watching directory: {organizer.base_path}")
    print(f"👀 Watching for new files in: {organizer.base_path} (Press CTRL+C to stop)")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logging.info("Stopped watching directory")
    observer.join()

# ENTRY POINT

def main() -> None:
    """
    Parse command-line argument and run the file organizer.
    """

    parser = argparse.ArgumentParser(
        description="Organize files in a directory into categorized subfolders."
    )
    parser.add_argument(
        "directory", type=str, help="Path to the directory you want to organize"
    )
    parser.add_argument(
        "--watch", action="store_true", help="Continuously watch and auto-organize files"
    )

    args = parser.parse_args()
    base_path = Path(args.directory)

    if not base_path.exists() or not base_path.is_dir():
        print("❌ Invalid directory path.")
        return
    
    organizer = FileOrganizer(base_path)
    organizer.organize_files()

    if args.watch:
        watch_directory(organizer)
    else:
        print("✅ Files have been organized successfully!")
        print(f"📜 Log saved to: {LOG_FILE}")


if __name__ == "__main__":
    main()