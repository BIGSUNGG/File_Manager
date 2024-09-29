import re
from Parse_Code import Utility

def parse_cs_file(file_path, old_name, new_name):
    """
    .cs 파일을 처리하여 ExtraModuleNames와 DependencyModuleNames에서
    old_name을 new_name으로 변경합니다.
    모듈 이름이 괄호로 둘러싸여 있을 경우 괄호를 유지합니다.

    :param file_path: 처리할 .cs 파일의 경로
    :param old_name: 기존 이름 (모듈 리스트에서 찾을 값)
    :param new_name: 새로운 이름 (모듈 리스트에서 변경할 값)
    """
    try:
        # 파일 읽기
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"파일 읽기 오류 ({file_path}): {e}")
        return

    file_modified = False  # 파일이 수정되었는지 여부

    # 처리할 패턴 목록
    patterns = [
        {
            'search': r'(ExtraModuleNames\s*\+\=\s*new\s+string\s*\[\]\s*\{\s*)([^}]+)(\s*\})',
            'module_name': 'ExtraModuleNames'
        },
        {
            'search': r'(DependencyModuleNames\.AddRange\s*\(\s*new\s+string\s*\[\]\s*\{\s*)([^}]+)(\s*\}\s*\)\s*;)',
            'module_name': 'DependencyModuleNames'
        }
    ]

    for pattern_info in patterns:
        search_pattern = pattern_info['search']  # 검색할 정규식 패턴
        module_name = pattern_info['module_name']  # 모듈 이름 (출력용)

        # 해당 패턴에 매칭되는 모든 부분 찾기
        matches = list(re.finditer(search_pattern, content))
        for match in matches:
            start = match.start(2)  # 모듈 리스트 시작 위치
            end = match.end(2)      # 모듈 리스트 끝 위치
            modules_str = content[start:end]  # 모듈 리스트 문자열 추출

            # 모듈 리스트를 개별 모듈로 분리
            modules = Utility.split_arguments(modules_str)
            modified_modules = []
            modified_this_section = False  # 현재 섹션에서 수정이 있었는지 여부

            for module in modules:
                # 모듈 이름을 앞뒤의 괄호와 내부 값으로 분리
                leading_parens, inner_value, trailing_parens = Utility.parse_argument(module)

                if inner_value == f'"{old_name}"':
                    inner_value = f'"{new_name}"'
                    modified_this_section = True
                    print(f"{file_path} 파일의 {module_name}에서 '{old_name}'를 '{new_name}'로 변경했습니다.")

                # 수정된 모듈 이름 재구성
                modified_module = leading_parens + inner_value + trailing_parens
                modified_modules.append(modified_module)

            if modified_this_section:
                # 변경된 모듈 리스트를 문자열로 변환
                new_modules_str = ', '.join(modified_modules)
                # 원본 콘텐츠에 변경 사항 적용
                content = content[:start] + new_modules_str + content[end:]
                file_modified = True

    if file_modified:
        try:
            # 변경된 내용 저장
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"{file_path} 파일이 수정되었습니다.")
        except Exception as e:
            print(f"파일 쓰기 오류 ({file_path}): {e}")
    else:
        print(f"{file_path} 파일에서 변경할 내용이 없습니다.")
