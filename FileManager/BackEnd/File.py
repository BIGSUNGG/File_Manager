import os
import re

# 파일에 있는 문자 변경
def parse_file(file_path, file_func):
    new_file_path = None     
    
    if file_func is not None:
        try:
            new_file_path = file_func(file_path)        
        except Exception as e:
            print(f"Error parsing file {file_path}: {e}")
        
    return file_path if new_file_path is None else new_file_path

def parse_folder(folder_path, folder_func): 
    # 폴더 이름 변경 
    new_folder_path = None
    
    if folder_func is not None:
        try:
            new_folder_path = folder_func(folder_path)        
        except Exception as e:
            print(f"Error parsing folder {folder_path}: {e}")
        
    return folder_path if new_folder_path is None else new_folder_path

def parse_files_and_folders(folder_path, file_func, folder_func):       
    new_folder_path = parse_folder(folder_path, folder_func)
    new_folder_path = folder_path if new_folder_path is None else new_folder_path

    if not os.path.exists(new_folder_path):
        return
    
    # 파일 및 폴더 탐색
    for entry in os.scandir(new_folder_path):
        if entry.is_file():  
            # 파일 탐색
            parse_file(entry.path, file_func)
        elif entry.is_dir():
            # 폴더 탐색
            parse_files_and_folders(entry.path, file_func, folder_func)                       
            
class Utility:
    @staticmethod
    def change_keword(file_path, old_keword, new_keyword):
        try:
            # 파일 열기
            with open(file_path, 'rb') as file:
                contents = file.read()
                
            # 변경될 문자열과 변경할 문자열 변경            
            updated_contents = re.sub((r'\b{0}\b').format(old_keword), new_keyword, contents)
            if updated_contents != contents:
                with open(file_path, 'wb') as file:
                    file.write(updated_contents)    
                    print(f"Update file {file_path}") 
        # 에러 발생 시
        except Exception as e:
            print(f"Error parsing file {file_path}: {e}")

    @staticmethod
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
                                                
            return new_file_path
        # 에러 발생 시
        except Exception as e:
            print(f"Error parsing file {file_path}: {e}")
            
        return None