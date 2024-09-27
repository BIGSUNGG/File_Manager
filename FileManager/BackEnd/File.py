import os

def rename_file(file_path, target_name):
    try:
        # 파일 이름 변경    
        new_file_path = os.path.dirname(file_path) + "\\" + target_name + ".uproject"
        if new_file_path != file_path and not os.path.exists(new_file_path):
            try:
                os.rename(file_path, new_file_path)
                print(f"Renamed file {file_path} to {new_file_path}")
            except Exception as e:
                print(f"Error renaming folder {file_path}: {e}")           
                                            
    # 에러 발생 시
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

# 파일에 있는 문자 변경
def process_file(file_path, old_bytes, new_bytes, change_file_content, change_file_name):
    try:
        # 파일 열기
        with open(file_path, 'rb') as file:
            contents = file.read()
            
        # 변경될 문자열과 변경할 문자열 변경            
        if(change_file_content):
            updated_contents = contents.replace(old_bytes, new_bytes)
            if updated_contents != contents:
                with open(file_path, 'wb') as file:
                    file.write(updated_contents)    
                    print(f"Update file {file_path}") 

        # 파일 이름 변경    
        if(change_file_name):           
            new_file_path = file_path.replace(old_bytes.decode('utf-8'), new_bytes.decode('utf-8'))
            if new_file_path != file_path and not os.path.exists(new_file_path):
                try:
                    os.rename(file_path, new_file_path)
                    print(f"Renamed file {file_path} to {new_file_path}")
                except Exception as e:
                    print(f"Error renaming folder {file_path}: {e}")           
                                            
    # 에러 발생 시
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

def process_folder(folder_path, old_bytes, new_bytes, change_folder_name): 
    # 폴더 이름 변경 
    if(change_folder_name):
        new_folder_path = folder_path.replace(old_bytes.decode('utf-8'), new_bytes.decode('utf-8'))
        if new_folder_path != folder_path and not os.path.exists(new_folder_path): 
            try:
                os.rename(folder_path, new_folder_path)
                print(f"Renamed folder {folder_path} to {new_folder_path}")
            except Exception as e:
                print(f"Error renaming folder {folder_path}: {e}")
        
        if not os.path.exists(new_folder_path):
            print(f"Error: The folder path {new_folder_path} does not exist.")
            
    return new_folder_path

def process_files_and_folders(folder_path, old_bytes, new_bytes, change_folder_name, search_child_folders, change_file_content, change_file_name, search_child_files): 
    new_folder_path = process_folder(folder_path, old_bytes, new_bytes, change_folder_name)
    
    if not os.path.exists(new_folder_path):
        return

    # 파일 및 폴더 탐색
    for entry in os.scandir(new_folder_path):
        if entry.is_file() and search_child_files:  
            # 파일 탐색
            process_file(entry.path, old_bytes, new_bytes, change_file_content, change_file_name)
        elif entry.is_dir() and search_child_folders:
            # 폴더 탐색
            process_files_and_folders(entry.path, old_bytes, new_bytes, change_folder_name, search_child_folders, change_file_content, change_file_name, search_child_files)           