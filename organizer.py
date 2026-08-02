import os
import shutil
from database import save_history
from logger import write_log
from datetime import datetime

# File categories
FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".pptx", ".xlsx"],
    "Videos": [".mp4", ".mkv", ".avi"],
    "Music": [".mp3", ".wav"],
    "Archives": [".zip", ".rar"]
}

def organize_files(folder_path):

    for file in os.listdir(folder_path):

        file_path = os.path.join(folder_path, file)

        # Skip folders
        if os.path.isdir(file_path):
            continue

        extension = os.path.splitext(file)[1].lower()

        moved = False

        for folder_name, extensions in FILE_TYPES.items():

            if extension in extensions:

                destination_folder = os.path.join(folder_path, folder_name)

                if not os.path.exists(destination_folder):
                    os.makedirs(destination_folder)

                new_path = os.path.join(destination_folder, file)

                shutil.move(file_path, new_path)

                save_history(
                    file,
                    file_path,
                    new_path,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )

                write_log(f"{file} moved to {destination_folder}")

                print(f"Moved: {file} -> {folder_name}")

                moved = True
                break

        if not moved:

            other_folder = os.path.join(folder_path, "Others")

            if not os.path.exists(other_folder):
                os.makedirs(other_folder)

            new_path = os.path.join(other_folder, file)

            shutil.move(file_path, new_path)

            save_history(
                file,
                file_path,
                new_path,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )

            write_log(f"{file} moved to Others")

            print(f"Moved: {file} -> Others")
            