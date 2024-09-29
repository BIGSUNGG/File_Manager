import os
import sys
import re
import os
import sys
import re

import Parse_Cpp as Cpp
import Parse_Cs as Cs

def parse_file(file_path):
    if not os.path.isfile(file_path):
        print(f"파일을 찾을 수 없습니다: {file_path}")
        sys.exit(1)

    if file_path.endswith('.cpp'):
        Cpp.parse_cpp_file(file_path)
    elif file_path.endswith('.cs'):
        Cs.parse_cs_file(file_path)
    else:
        print("지원하지 않는 파일 형식입니다. .cpp 또는 .cs 파일을 입력해주세요.")

class Utility:
    @staticmethod
    def find_matching_paren(s, start):
        """
        여는 괄호 '('의 위치에서 시작하여 해당되는 닫는 괄호 ')'의 위치를 찾습니다.
        문자열 리터럴과 이스케이프 문자를 고려하여 올바른 괄호 매칭을 수행합니다.

        :param s: 전체 문자열
        :param start: 여는 괄호 '('의 인덱스
        :return: 대응되는 닫는 괄호 ')'의 인덱스, 없으면 -1 반환
        """
        assert s[start] == '(', "find_matching_paren 함수는 여는 괄호에서 시작해야 합니다."
        depth = 1  # 괄호의 깊이 (중첩 수준)
        in_string = False  # 현재 문자열 리터럴 내부인지 여부
        escape = False  # 이스케이프 문자 처리 여부

        for i in range(start + 1, len(s)):
            c = s[i]

            if escape:
                escape = False  # 이스케이프 문자 다음 문자는 그대로 처리
                continue

            if c == '\\':
                escape = True  # 다음 문자는 이스케이프 처리
                continue

            if c == '"':
                in_string = not in_string  # 문자열 리터럴의 시작 또는 종료
                continue

            if in_string:
                continue  # 문자열 내부에서는 괄호를 무시

            if c == '(':
                depth += 1  # 여는 괄호 발견 시 깊이 증가
            elif c == ')':
                depth -= 1  # 닫는 괄호 발견 시 깊이 감소
                if depth == 0:
                    return i  # 깊이가 0이면 대응되는 닫는 괄호를 찾은 것

        return -1  # 닫는 괄호를 찾지 못한 경우

    @staticmethod
    def split_arguments(arg_str):
        """
        함수나 매크로의 인자 문자열을 파싱하여 개별 인자들의 리스트로 반환합니다.
        문자열 리터럴, 괄호의 중첩, 이스케이프 문자 등을 고려하여 정확한 분리를 수행합니다.

        :param arg_str: 인자 문자열
        :return: 인자들의 리스트
        """
        args = []  # 결과로 반환할 인자 리스트
        current = ''  # 현재 처리 중인 인자 문자열
        depth = 0  # 괄호의 깊이
        in_string = False  # 현재 문자열 리터럴 내부인지 여부
        escape = False  # 이스케이프 문자 처리 여부

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
                # 깊이가 0이고 문자열 리터럴이 아닌 상태에서의 콤마는 인자 분리를 의미
                args.append(current.strip())
                current = ''
                continue

            if c == '(':
                depth += 1  # 여는 괄호 발견 시 깊이 증가
            elif c == ')':
                depth -= 1  # 닫는 괄호 발견 시 깊이 감소

            current += c  # 현재 문자 추가

        if current.strip():
            args.append(current.strip())  # 마지막 인자 추가

        return args

    @staticmethod
    def parse_argument(arg):
        """
        개별 인자를 앞쪽의 괄호, 내부 값, 뒤쪽의 괄호로 분리합니다.

        :param arg: 개별 인자 문자열
        :return: (leading_parens, inner_value, trailing_parens)의 튜플
        """
        # 앞쪽 공백 제거
        arg = arg.lstrip()
        leading_parens = ''
        # 여는 괄호를 모두 추출
        while arg.startswith('('):
            leading_parens += '('
            arg = arg[1:]

        # 뒤쪽 공백 제거
        arg = arg.rstrip()
        trailing_parens = ''
        # 닫는 괄호를 모두 추출
        while arg.endswith(')'):
            trailing_parens = ')' + trailing_parens
            arg = arg[:-1]

        # 남은 부분이 내부 값
        inner_value = arg.strip()

        return leading_parens, inner_value, trailing_parens

