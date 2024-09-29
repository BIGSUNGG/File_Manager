import re
from Parse_Code import Utility

def parse_cpp_file(file_path, old_name, new_name):
    """
    .cpp 파일을 처리하여 IMPLEMENT_PRIMARY_GAME_MODULE 매크로의 인자를 변경합니다.
    두 번째 인자가 old_name인 경우 new_name으로,
    세 번째 인자가 old_name인 경우 new_name으로 변경합니다.
    인자가 괄호로 둘러싸여 있어도 괄호를 유지합니다.

    :param file_path: 처리할 .cpp 파일의 경로
    :param old_name: 기존 이름 (두 번째 또는 세 번째 인자에서 찾을 값)
    :param new_name: 새로운 이름 (두 번째 또는 세 번째 인자를 변경할 값)
    """
    try:
        # 파일 읽기
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"파일 읽기 오류 ({file_path}): {e}")
        return

    modified = False  # 파일이 수정되었는지 여부
    idx = 0  # 현재 검색 위치

    while True:
        # IMPLEMENT_PRIMARY_GAME_MODULE 매크로를 찾는 정규식 패턴
        match = re.search(r'IMPLEMENT_PRIMARY_GAME_MODULE\s*\(', content[idx:])
        if not match:
            break  # 더 이상 매칭되는 패턴이 없음

        start = idx + match.start()  # 매크로 시작 위치
        paren_start = content.find('(', start)  # 여는 괄호 위치
        paren_end = Utility.find_matching_paren(content, paren_start)  # 닫는 괄호 위치

        if paren_end == -1:
            print(f"괄호를 찾을 수 없습니다: {file_path}")
            idx = start + 1
            continue

        # 매크로의 인자 부분 추출
        args_str = content[paren_start+1:paren_end]
        # 인자를 개별적으로 파싱
        args = Utility.split_arguments(args_str)
        modified_args = []
        modified_this_call = False  # 현재 매크로 호출에서 수정이 있었는지 여부

        for i, arg in enumerate(args):
            # 인자를 앞뒤의 괄호와 내부 값으로 분리
            leading_parens, inner_value, trailing_parens = Utility.parse_argument(arg)

            # 두 번째 인자 처리
            if i == 1 and inner_value == old_name:
                inner_value = new_name
                modified = True
                modified_this_call = True
                print(f"파일 '{file_path}'에서 두 번째 인자의 값을 '{new_name}'으로 변경했습니다.")

            # 세 번째 인자 처리
            if i == 2 and inner_value == f'"{old_name}"':
                inner_value = f'"{new_name}"'
                modified = True
                modified_this_call = True
                print(f"파일 '{file_path}'에서 세 번째 인자의 값을 '\"{new_name}\"'으로 변경했습니다.")

            # 수정된 인자 재구성
            modified_arg = leading_parens + inner_value + trailing_parens
            modified_args.append(modified_arg)

        if modified_this_call:
            # 변경 사항 적용
            new_args_str = ', '.join(modified_args)
            content = content[:paren_start+1] + new_args_str + content[paren_end:]
            idx = paren_start + len(new_args_str) + 1  # 다음 검색 위치 업데이트
        else:
            idx = paren_end + 1  # 변경이 없으면 다음 위치로 이동

    if modified:
        try:
            # 변경된 내용 저장
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"{file_path} 파일이 수정되었습니다.")
        except Exception as e:
            print(f"파일 쓰기 오류 ({file_path}): {e}")
    else:
        print(f"{file_path} 파일에서 변경할 내용이 없습니다.")
