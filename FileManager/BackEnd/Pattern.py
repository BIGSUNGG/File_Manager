import os
import sys
import re

class PatternInfo:
    search = None
    item_name = None
    old_name = None
    new_name = None
    args_to_check = None

def parse_Pattern(file_path, patterns):
    if not os.path.isfile(file_path):
        print(f"파일을 찾을 수 없습니다: {file_path}")
        sys.exit(1)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"파일 읽기 오류 ({file_path}): {e}")
        sys.exit(1)

    modified = False

    for pattern_info in patterns:
        # 패턴에서 old_name과 new_name을 포함하도록 수정
        search_pattern = pattern_info.search.format(
            old_name=re.escape(pattern_info.old_name) if pattern_info.old_name else '',
            new_name=re.escape(pattern_info.new_name) if pattern_info.new_name else ''
        )
        item_name = pattern_info.item_name
        args_to_check = pattern_info.args_to_check or []
        old_name = pattern_info.old_name or ''
        new_name = pattern_info.new_name or ''

        # 해당 패턴에 매칭되는 모든 부분 찾기
        matches = list(re.finditer(search_pattern, content, re.DOTALL))
        for match in matches:
            start = match.start(2)
            end = match.end(2)
            args_str = content[start:end]

            # 인자를 개별적으로 파싱
            args = Utility.split_arguments(args_str)
            modified_args = []
            modified_this_call = False

            for i, arg in enumerate(args):
                leading_parens, inner_value, trailing_parens = Utility.parse_argument(arg)

                if args_to_check:
                    if i in args_to_check:
                        if old_name and (inner_value == old_name or inner_value == f'"{old_name}"'):
                            inner_value = f'"{new_name}"' if inner_value.startswith('"') else new_name
                            modified_this_call = True
                            print(f"파일 '{file_path}'에서 '{item_name}'의 인자 {i+1}을(를) '{new_name}'으로 변경했습니다.")
                else:
                    if old_name and (inner_value == old_name or inner_value == f'"{old_name}"'):
                        inner_value = f'"{new_name}"' if inner_value.startswith('"') else new_name
                        modified_this_call = True
                        print(f"파일 '{file_path}'에서 '{item_name}'의 인자 {i+1}을(를) '{new_name}'으로 변경했습니다.")

                modified_arg = leading_parens + inner_value + trailing_parens
                modified_args.append(modified_arg)

            if modified_this_call:
                # 변경된 인자 리스트를 문자열로 변환
                new_args_str = ', '.join(modified_args)
                # 원본 콘텐츠에 변경 사항 적용
                content = content[:start] + new_args_str + content[end:]
                modified = True

    if modified:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"{file_path} 파일이 수정되었습니다.")
        except Exception as e:
            print(f"파일 쓰기 오류 ({file_path}): {e}")
    else:
        print(f"{file_path} 파일에서 변경할 내용이 없습니다.")
    
class Utility:
    @staticmethod
    def split_arguments(arg_str):
        """
        함수나 매크로의 인자 문자열을 파싱하여 개별 인자들의 리스트로 반환합니다.
        문자열 리터럴, 괄호의 중첩, 이스케이프 문자 등을 고려하여 정확한 분리를 수행합니다.
        
        :param arg_str: 인자 문자열
        :return: 인자들의 리스트
        """
        args = []
        current = ''
        depth = 0
        in_string = False
        escape = False

        for c in arg_str:
            if escape:
                current += c
                escape = False
                continue

            if c == '\\':
                current += c
                escape = True
                continue

            if c == '"':
                current += c
                in_string = not in_string
                continue

            if in_string:
                current += c
                continue

            if c == ',' and depth == 0:
                args.append(current.strip())
                current = ''
                continue

            if c == '(':
                depth += 1
            elif c == ')':
                depth -= 1

            current += c

        if current.strip():
            args.append(current.strip())

        return args

    @staticmethod
    def parse_argument(arg):
        """
        개별 인자를 앞쪽의 괄호, 내부 값, 뒤쪽의 괄호로 분리합니다.
        
        :param arg: 개별 인자 문자열
        :return: (leading_parens, inner_value, trailing_parens)의 튜플
        """
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
