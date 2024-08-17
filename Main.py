import os

# 파일에 있는 문자 변경
def replace_bytes_in_file(file_path, old_bytes, new_bytes):
    try:
        # 파일 열기
        with open(file_path, 'rb') as file:
            contents = file.read()
            
        # 변경될 문자열과 변경할 문자열 변경            
        if(change_fileContent):
            updated_contents = contents.replace(old_bytes, new_bytes)
            if updated_contents != contents:
                with open(file_path, 'wb') as file:
                    file.write(updated_contents)    
                    print(f"Update file {file_path}") 

        # 파일 이름 변경    
        if(change_fileName):            
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

def process_files_and_folders(folder_path, old_bytes, new_bytes): 
    # 폴더 이름 변경 
    if(change_folderName):
        new_folder_path = folder_path.replace(old_bytes.decode('utf-8'), new_bytes.decode('utf-8'))
        if new_folder_path != folder_path and not os.path.exists(new_folder_path): 
            try:
                os.rename(folder_path, new_folder_path)
                print(f"Renamed folder {folder_path} to {new_folder_path}")
            except Exception as e:
                print(f"Error renaming folder {folder_path}: {e}")
        
        if not os.path.exists(new_folder_path):
            print(f"Error: The folder path {new_folder_path} does not exist.")
            return

    # 파일 및 폴더 탐색
    for entry in os.scandir(new_folder_path):
        if entry.is_file():  
            # 파일 탐색
            replace_bytes_in_file(entry.path, old_bytes, new_bytes)
        elif search_child_folders and entry.is_dir():
            # 폴더 탐색
            process_files_and_folders(entry.path, old_bytes, new_bytes)

# 폴더 경로
folder_path = r'C:\Important\Project\Unreal Project\FPS' 
# 변경할 문자열
old_bytes = b'KRAVER'
# 변경될 문자열
new_bytes = b'FPS'

# 파일 내용을 변경할지
change_fileContent = True;
# 파일 이름을 변경할지
change_fileName = True;
# 폴더 이름을 변경할지
change_folderName = True;
# 폴더안에 있는 다른 하위 폴더들도 탐색할지
search_child_folders = True;

process_files_and_folders(folder_path, old_bytes, new_bytes)