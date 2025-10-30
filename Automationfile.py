
import os
import shutil

# --- File type categories ---
FILE_CATEGORIES = {
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".ppt", ".pptx", ".xls", ".xlsx", ".rtf", ".odt"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".tiff", ".ico"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi", ".flv", ".wmv", ".webm", ".m4v", ".3gp"],
    "Music": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a", ".wma", ".aiff"],
    "Archives": [".zip", ".rar", ".tar", ".gz", ".7z", ".bz2", ".xz"],
    "Programs": [".exe", ".msi", ".dmg", ".pkg", ".deb", ".rpm"],
    "Code": [".py", ".java", ".cpp", ".c", ".html", ".css", ".js", ".php", ".json", ".xml"],
    "Spreadsheets": [".csv", ".xls", ".xlsx", ".ods"],
    "Presentations": [".ppt", ".pptx", ".key", ".odp"],
}


def organize_files(target_folder):
    """
    Organizes files in the given folder into subfolders by file type.
    
    Args:
        target_folder (str): Path to the folder that needs to be organized
    """
    # Validate if folder exists
    if not os.path.exists(target_folder):
        print(f"Error: The folder '{target_folder}' does not exist.")
        return

    # Validate if path is a directory
    if not os.path.isdir(target_folder):
        print(f"Error: '{target_folder}' is not a directory.")
        return

    print(f"📁 Organizing files in: {target_folder}")
    
    # Create subfolders if not present
    for folder in FILE_CATEGORIES.keys():
        folder_path = os.path.join(target_folder, folder)
        os.makedirs(folder_path, exist_ok=True)
    
    # Create Others folder for uncategorized files
    others_path = os.path.join(target_folder, "Others")
    os.makedirs(others_path, exist_ok=True)

    # Counters for statistics
    moved_files = 0
    skipped_files = 0

    # Go through each file in the directory
    for filename in os.listdir(target_folder):
        file_path = os.path.join(target_folder, filename)

        # Skip directories and hidden files
        if os.path.isdir(file_path) or filename.startswith('.'):
            skipped_files += 1
            continue

        # Get file extension
        _, ext = os.path.splitext(filename)
        ext = ext.lower()

        # Skip files without extensions
        if not ext:
            dest_path = os.path.join(others_path, filename)
            shutil.move(file_path, dest_path)
            moved_files += 1
            continue

        # Determine the destination folder
        moved = False
        for category, extensions in FILE_CATEGORIES.items():
            if ext in extensions:
                dest_folder = os.path.join(target_folder, category)
                dest_path = os.path.join(dest_folder, filename)
                
                # Handle file name conflicts
                counter = 1
                name, extension = os.path.splitext(filename)
                while os.path.exists(dest_path):
                    new_filename = f"{name}_{counter}{extension}"
                    dest_path = os.path.join(dest_folder, new_filename)
                    counter += 1
                
                shutil.move(file_path, dest_path)
                moved = True
                moved_files += 1
                break

        # If file type is unknown, move to Others
        if not moved:
            dest_path = os.path.join(others_path, filename)
            shutil.move(file_path, dest_path)
            moved_files += 1

    # Print summary
    print(f"Organization complete!")
    print(f"Files moved: {moved_files}")
    print(f"Files skipped: {skipped_files}")


def preview_organization(target_folder):
    """
    Preview what files will be moved where without actually moving them.
    
    Args:
        target_folder (str): Path to the folder to preview
    """
    if not os.path.exists(target_folder):
        print(f"Error: The folder '{target_folder}' does not exist.")
        return

    print(f"🔍 Preview organization for: {target_folder}")
    print("-" * 50)
    
    organization_plan = {}

    for filename in os.listdir(target_folder):
        file_path = os.path.join(target_folder, filename)

        if os.path.isdir(file_path) or filename.startswith('.'):
            continue

        _, ext = os.path.splitext(filename)
        ext = ext.lower()

        category = "Others"
        for cat, extensions in FILE_CATEGORIES.items():
            if ext in extensions:
                category = cat
                break

        if category not in organization_plan:
            organization_plan[category] = []
        organization_plan[category].append(filename)

    # Display preview
    for category, files in organization_plan.items():
        print(f"\n📂 {category} ({len(files)} files):")
        for file in files:
            print(f"   └── {file}")

    if not organization_plan:
        print("No files found to organize.")


# --- Example usage ---
#if _name_ == "_main_":
    #print("File Organizer")
    #print("=" * 40)
    
target_path = input("Enter the path of the folder to organize: ").strip()
    
    # Remove quotes if user pasted path with quotes
target_path = target_path.strip('"').strip("'")
    
    # Ask user if they want to preview first
choice = input("\nDo you want to preview before organizing? (y/n): ").strip().lower()
    
if choice == 'y' or choice == 'yes':
    preview_organization(target_path)
    confirm = input("\nProceed with organization? (y/n): ").strip().lower()
    if confirm == 'y' or confirm == 'yes':
        organize_files(target_path)
    else:
        print("Organization cancelled.")
else:
    organize_files(target_path)
