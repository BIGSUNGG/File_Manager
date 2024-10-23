import re
import os

from Utility import ContentUtility as ContentUtility
from Utility import FileUtility as FileUtility

class Pattern:
    class PatternInfo:
        def __init__(self, search, item_name, old_name, new_name, args_to_check=None):
            self.search = search
            self.item_name = item_name
            self.old_name = old_name
            self.new_name = new_name
            self.args_to_check = args_to_check

    @staticmethod
    def parse_pattern(file_content, patterns):
        content = file_content
        modified = False

        for pattern_info in patterns:
            # 패턴에서 old_name과 new_name을 설정
            search_pattern = pattern_info.search.format(
                old_name=re.escape(pattern_info.old_name) if pattern_info.old_name else '',
                new_name=re.escape(pattern_info.new_name) if pattern_info.new_name else ''
            )
            item_name = pattern_info.item_name
            args_to_check = pattern_info.args_to_check or []
            old_name = pattern_info.old_name or ''
            new_name = pattern_info.new_name or ''

            # 패턴에 매칭되는 모든 부분 찾기
            matches = list(re.finditer(search_pattern, content, re.DOTALL))
            for match in matches:
                # 매칭된 인자 부분 추출
                if 'args' in match.groupdict() and match.group('args'):
                    start = match.start('args')
                    end = match.end('args')
                    args_str = content[start:end]

                    # 인자와 위치 정보 파싱
                    args = ContentUtility.split_arguments(args_str)
                    new_args_pieces = []
                    last_end = 0
                    modified_this_call = False

                    for i, arg_dict in enumerate(args):
                        arg = arg_dict['arg']
                        arg_start = arg_dict['start']
                        arg_end = arg_dict['end']

                        # 이전 인자와 현재 인자 사이의 구분자 추가 (줄 바꿈과 공백 유지)
                        new_args_pieces.append(args_str[last_end:arg_start])

                        leading_parens, inner_value, trailing_parens = ContentUtility.parse_argument(arg)

                        if args_to_check:
                            if i in args_to_check:
                                if old_name and (inner_value == old_name or inner_value == f'"{old_name}"'):
                                    inner_value = f'"{new_name}"' if inner_value.startswith('"') else new_name
                                    modified_this_call = True
                                    print(f"'{item_name}'의 인자 {i+1}을 '{new_name}'으로 변경")
                        else:
                            if old_name and (inner_value == old_name or inner_value == f'"{old_name}"'):
                                inner_value = f'"{new_name}"' if inner_value.startswith('"') else new_name
                                modified_this_call = True
                                print(f"'{item_name}'의 인자 {i+1}을 '{new_name}'으로 변경")

                        # 변경된 인자 추가
                        modified_arg = leading_parens + inner_value + trailing_parens
                        new_args_pieces.append(modified_arg)
                        last_end = arg_end

                    # 마지막 인자 이후의 내용 추가
                    new_args_pieces.append(args_str[last_end:])

                    if modified_this_call:
                        # 변경된 인자 문자열로 재구성 (포맷 유지)
                        new_args_str = ''.join(new_args_pieces)
                        # 원본 콘텐츠에 변경 사항 적용
                        content = content[:start] + new_args_str + content[end:]
                        modified = True

        if modified:
            print("파일 내용이 수정됨")
            return content
        else:
            print("변경할 내용이 없음")
            return file_content

class Config:
    @staticmethod
    def find_section(lines, section_name):
        """
        주어진 라인 리스트에서 특정 섹션의 시작 인덱스를 찾음

        :param lines: 파일의 라인 리스트
        :param section_name: 찾고자 하는 섹션 이름
        :return: 섹션 시작 인덱스 또는 None
        """
        for index, line in enumerate(lines):
            stripped_line = line.strip()
            if stripped_line.startswith('[') and stripped_line.endswith(']'):
                current_section = stripped_line[1:-1].strip()
                if current_section == section_name:
                    return index
        return None

    @staticmethod
    def add_or_update_key_in_section(lines, section_start_index, key_name, value, force_add=False):
        """
        섹션 내부에서 키의 값을 추가하거나 업데이트
        force_add가 True이면, 키가 이미 존재해도 새로운 키-값 쌍을 추가

        :param lines: 파일의 라인 리스트
        :param section_start_index: 섹션의 시작 인덱스
        :param key_name: 추가하거나 업데이트할 키 이름
        :param value: 설정할 값
        :param force_add: True이면 키가 존재해도 새로운 키-값 쌍을 추가
        """
        index = section_start_index + 1
        key_found = False
        while index < len(lines):
            line = lines[index]
            stripped_line = line.strip()
            if stripped_line.startswith('[') and stripped_line.endswith(']'):
                break  # 다음 섹션이 시작되면 종료
            if '=' in stripped_line:
                key = stripped_line.split('=', 1)[0].strip()
                if key == key_name:
                    if not force_add:
                        # 키를 찾았으므로 값을 업데이트하고 함수 종료
                        lines[index] = f'{key_name}={value}\n'
                        key_found = True
                        return
            index += 1
        if not key_found or force_add:
            # 키를 찾지 못했거나 force_add가 True인 경우 섹션의 끝에 새로운 키-값 쌍 추가
            # 섹션의 끝을 찾아 삽입 위치 결정
            insert_index = index
            while insert_index > section_start_index + 1 and lines[insert_index - 1].strip() == '':
                insert_index -= 1
            lines.insert(insert_index, f'{key_name}={value}\n')

        return lines

    @staticmethod
    def add_section_with_key(lines, section_name, key_name, value):
        """
        새로운 섹션을 추가하고 키-값 쌍을 설정

        :param lines: 파일의 라인 리스트
        :param section_name: 추가할 섹션 이름
        :param key_name: 설정할 키 이름
        :param value: 설정할 값
        """
        # 파일 끝에 새로운 섹션과 키-값 쌍 추가
        lines.append(f'\n[{section_name}]\n')
        lines.append(f'{key_name}={value}\n')

    @staticmethod
    def parse_config(file_content, section_to_find, key_to_find, new_value, force_add=False):
        """
        설정 파일 내용을 파싱하여 특정 섹션과 키의 값을 업데이트하거나 추가
        force_add가 True이면, 키가 존재해도 새로운 키-값 쌍을 추가

        :param file_content: 설정 파일의 전체 내용 (문자열)
        :param section_to_find: 값을 변경하거나 추가할 섹션 이름
        :param key_to_find: 값을 변경하거나 추가할 키 이름
        :param new_value: 설정할 새로운 값
        :param force_add: True이면 키가 존재해도 새로운 키-값 쌍을 추가
        :return: 변경된 파일 내용
        """
        try:
            lines = file_content.splitlines(keepends=True)
            section_index = Config.find_section(lines, section_to_find)

            if section_index is not None:
                # 섹션을 찾은 경우 키를 추가하거나 업데이트
                Config.add_or_update_key_in_section(lines, section_index, key_to_find, new_value, force_add)
            else:
                # 섹션을 찾지 못한 경우 새로운 섹션과 키를 추가
                Config.add_section_with_key(lines, section_to_find, key_to_find, new_value)

            # 변경된 내용을 문자열로 반환
            return ''.join(lines)
        except Exception as e:
            print(f"내용 파싱 중 오류 발생: {e}")
            return file_content  # 오류 발생 시 원본 내용 반환

class File:
    # 파일의 문자 변경 함수
    def parse_file(file_path, file_func):
        new_file_path = None  # 변경된 파일 경로 저장 변수
    
        if file_func is not None:
            try:
                new_file_path = file_func(file_path)  # 파일 변환 함수 적용
            except Exception as e:
                print(f"파일 {file_path} 파싱 중 오류 발생: {e}")
            
        return file_path if new_file_path is None else new_file_path  # 변경되지 않았으면 원본 경로 반환

    # 폴더 이름 변경 함수
    def parse_folder(folder_path, folder_func): 
        new_folder_path = None  # 변경된 폴더 경로 저장 변수
    
        if folder_func is not None:
            try:
                new_folder_path = folder_func(folder_path)  # 폴더 변환 함수 적용
            except Exception as e:
                print(f"폴더 {folder_path} 파싱 중 오류 발생: {e}")
            
        return folder_path if new_folder_path is None else new_folder_path  # 변경되지 않았으면 원본 경로 반환

    # 폴더 내 모든 파일과 하위 폴더를 탐색하고 변환 적용 함수
    def parse_files_and_folders(folder_path, file_func, folder_func):       
        new_folder_path = File.parse_folder(folder_path, folder_func)  # 폴더 경로 변환
        new_folder_path = folder_path if new_folder_path is None else new_folder_path  # 변환되지 않았으면 원본 경로 유지

        if not os.path.exists(new_folder_path):
            return  # 변환된 폴더가 없으면 종료
    
        # 폴더 내 파일 및 폴더 탐색
        for entry in os.scandir(new_folder_path):
            if entry.is_file():  
                File.parse_file(entry.path, file_func)  # 파일 변환 함수 적용
            elif entry.is_dir():
                File.parse_files_and_folders(entry.path, file_func, folder_func)  # 하위 폴더 재귀 탐색
