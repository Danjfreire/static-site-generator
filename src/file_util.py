import os
import shutil

def clear_directory(directory:str):
    if os.path.exists(directory) and os.path.isdir(directory):
        files = os.listdir(directory)

        for filename in files:
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                os.unlink(file_path)
                print(f"Removing file: {file_path}")
            elif os.path.isdir(file_path):
                clear_directory(file_path)

    is_sub_dir = os.path.sep in directory
    if is_sub_dir:
        print(f"Removing dir:", directory)
        os.rmdir(directory)



def copy_files(source:str, target:str):
    print(f"Clearing target directory: {target}")
    clear_directory(target)

    # Create target dir if it doesnt exists
    if not os.path.exists(target):
        os.makedirs(target)
    
    if os.path.exists(source) and os.path.isdir(source):
        files = os.listdir(source)

        for filename in files:
            source_path = os.path.join(source, filename)
            target_path = os.path.join(target, filename)

            if os.path.isfile(source_path):
                shutil.copy(source_path, target_path)
                print(f"Copied file: {source_path} -> {target_path}")
            elif os.path.isdir(source_path):
                shutil.copytree(source_path, target_path)
                print(f"Copied directory: {source_path}i -> {target_path}")
    else:
        print(f"Target directory {source} does not exist")
