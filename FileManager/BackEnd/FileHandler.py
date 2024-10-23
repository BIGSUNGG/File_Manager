import os

class FileHandler:
    def __init__(self, file_path):
        self.file_path = file_path
        self.origin_content = ''
        self.change_content = ''
        
    def read_file(self):
        if not os.path.isfile(self.file_path):
            print(f"파일을 찾을 수 없습니다: {self.file_path}")
            return 

        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.origin_content = f.read()
                self.change_content = self.origin_content[:]
        except Exception as e:
            print(f"파일 읽기 오류 ({self.file_path}): {e}")
            return 
    
    def write_file(self):
        if not os.path.isfile(self.file_path):
            print(f"파일을 찾을 수 없습니다: {self.file_path}")
            return 
        
        modified = self.origin_content is not self.change_content
        if(modified is True):
            try:
                with open(self.file_path, 'w', encoding='utf-8') as f:
                    f.write(self.change_content)
                    print("변경점 저장")
            except Exception as e:
                print(f"파일 쓰기 오류 ({self.file_path}): {e}")
        else:
            print("변경점 없음")
            
    def action_content(self, action_func):
        self.change_content = action_func(self.change_content)
        
    def action_path(self, action_func):
        self.file_path = action_func(self.file_path)
