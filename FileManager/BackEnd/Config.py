#import configparser : 섹션 이름이 -로 시작하면 읽지 못하는 문제가 있어 사용하지 않음

def parse_config(file_path, section_to_find, key_to_find, new_value):
    # 파일을 읽기 모드로 엽니다
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        
    current_section = None  # 현재 섹션을 추적할 변수
    found_section = False  # 찾고 있는 섹션을 발견했는지 여부
    key_found = False  # 키를 찾았는지 여부
    
    # 파일의 각 라인을 순회합니다
    for index, line in enumerate(lines):
        stripped_line = line.strip()  # 앞뒤 공백 제거
        # 만약 라인이 섹션 헤더([섹션])이면
        if stripped_line.startswith('[') and stripped_line.endswith(']'):
            current_section = stripped_line[1:-1].strip()  # 섹션 이름을 가져옴
            found_section = (current_section == section_to_find)  # 찾고자 하는 섹션인지 확인
        elif found_section:
            # 키-값 쌍이 있는 라인인지 확인
            if '=' in stripped_line:
                key_value = stripped_line.split('=', 1)  # '='로 나누어 키와 값을 분리
                key = key_value[0].strip()
                if key == key_to_find:
                    # 키를 찾았으므로 값을 업데이트
                    lines[index] = f'{key}={new_value}\n'
                    key_found = True  # 키를 찾았음을 기록
                    found_section = False  # 업데이트 후 섹션 탐색 종료
            # 주석이나 빈 줄은 건너뜁니다
            elif not stripped_line or stripped_line.startswith(';') or stripped_line.startswith('#'):
                continue
            else:
                # 섹션이 끝났다고 간주
                found_section = False
        
    if not key_found:
        # 키를 찾지 못한 경우 키를 섹션에 추가해야 함
        section_found = False
        for index, line in enumerate(lines):
            stripped_line = line.strip()
            # 섹션을 다시 탐색
            if stripped_line.startswith('[') and stripped_line.endswith(']'):
                current_section = stripped_line[1:-1].strip()
                if current_section == section_to_find:
                    section_found = True
                    # 새로운 키-값 쌍을 삽입할 위치를 찾습니다
                    insert_index = index + 1
                    # 섹션의 끝 또는 다음 섹션 헤더까지 이동
                    while insert_index < len(lines):
                        next_line = lines[insert_index]
                        next_line_stripped = next_line.strip()
                        if next_line_stripped.startswith('[') and next_line_stripped.endswith(']'):
                            # 다음 섹션이 시작되면 그 전에 삽입
                            break
                        insert_index += 1
                    # 섹션 끝에 있는 빈 줄을 건너뜁니다
                    while insert_index > index + 1 and lines[insert_index - 1].strip() == '':
                        insert_index -= 1
                    # 새로운 키-값 쌍 삽입
                    lines.insert(insert_index, f'{key_to_find}={new_value}\n')
                    break
        if not section_found:
            # 섹션을 찾지 못했을 경우 파일의 끝에 새로운 섹션과 함께 추가
            lines.append(f'\n[{section_to_find}]\n')
            lines.append(f'{key_to_find}={new_value}\n')
        
    # 파일에 변경된 내용을 다시 씁니다
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)

