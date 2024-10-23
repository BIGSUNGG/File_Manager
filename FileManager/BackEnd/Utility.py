import os
import re

def string_to_bytes(str):
    return str.encode('utf-8')
            
class FileUtility:                    
    @staticmethod
    def rename_file(file_path, new_name):
        try:
            # 파일 이름을 새로운 이름으로 변경
            new_file_path = os.path.join(os.path.dirname(file_path), f"{new_name}")
            if new_file_path != file_path and not os.path.exists(new_file_path):
                try:
                    os.rename(file_path, new_file_path)  # 파일 이름 변경
                    print(f"파일 이름을 {file_path}에서 {new_file_path}로 변경")
                except Exception as e:
                    print(f"파일 {file_path} 이름 변경 중 오류 발생: {e}")           
                                                    
            return new_file_path  # 변경된 파일 경로 반환
        except Exception as e:
            print(f"파일 {file_path} 파싱 중 오류 발생: {e}")
                
        return None  # 오류 발생 시 None 반환
               
    @staticmethod
    def get_base_path(file_path):
        return os.path.dirname(file_path)

    @staticmethod
    def get_base_name(file_path):
        return os.path.basename(file_path)    

class ContentUtility:
    @staticmethod
    def change_keyword(file_content, old_keyword, new_keyword): 
        # 특정 키워드를 새로운 키워드로 변경
        updated_contents = re.sub(rf'\b{re.escape(old_keyword)}\b', new_keyword, file_content)
        return updated_contents  # 변경된 내용 반환
    
    @staticmethod
    def split_arguments(arg_str):
        # 인자 문자열을 개별 인자와 위치 정보로 나누기
        args = []
        current = ''
        depth = 0
        in_string = False
        escape = False
        arg_start = 0
        i = 0

        while i < len(arg_str):
            c = arg_str[i]
            if escape:
                current += c
                escape = False
                i += 1
                continue

            if c == '\\':
                current += c
                escape = True
                i += 1
                continue

            if c == '"':
                current += c
                in_string = not in_string
                i += 1
                continue

            if in_string:
                current += c
                i += 1
                continue

            if c == ',' and depth == 0:
                # 인자 종료 위치 저장
                arg_end = i
                args.append({'arg': current.strip(), 'start': arg_start, 'end': arg_end})
                current = ''
                i += 1
                # 다음 인자의 시작 위치 설정 (공백 포함 가능)
                while i < len(arg_str) and arg_str[i].isspace():
                    i += 1
                arg_start = i
                continue

            if c == '(':
                depth += 1
            elif c == ')':
                depth -= 1

            current += c
            i += 1

        if current.strip():
            # 마지막 인자 추가
            arg_end = i
            args.append({'arg': current.strip(), 'start': arg_start, 'end': arg_end})

        return args

    @staticmethod
    def parse_argument(arg):
        # 인자를 괄호로 분리
        arg = arg.lstrip()
        leading_parens = ''
        while arg.startswith('('):
            leading_parens += '('
            arg = arg[1:]

        arg = arg.rstrip()
        trailing_parens = ''
        while arg.endswith(')'):
            trailing_parens = ')' + trailing_parens
            arg = arg[:-1]

        inner_value = arg.strip()
        return leading_parens, inner_value, trailing_parens
