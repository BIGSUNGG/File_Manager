<h2>File Manager 프로젝트</h2>

File Manager 프로젝트는 `.NET MAUI`와 `IronPython`을 사용한 언리얼 엔진 프로젝트 관리 프로젝트입니다.  

---

<h3>기술 스택</h3>

---

<table align="center">
    <tr align="center">
        <td style="font-weight: bold; padding-right: 10px; vertical-align: center;">
            언어
        </td>
        <td>
            <img height="40" src="https://cdn.worldvectorlogo.com/logos/c--4.svg"/> 
            <img height="40" src="https://cdn.iconscout.com/icon/free/png-256/free-python-3521655-2945099.png?f=webp"/>
        </td>
    </tr>
    <tr align="center">
        <td style="font-weight: bold; padding-right: 10px; vertical-align: center; border: none;">
        프론트엔드
        </td>
        <td>
            <img height="40" src="https://skillicons.dev/icons?i=html,css"/>
            <img height="40" src="https://devblogs.microsoft.com/aspnet/wp-content/uploads/sites/16/2019/04/BrandBlazor_nohalo_1000x.png"/>
        </td>
    </tr>
</table>

<h2>구현된 기능</h2>

1. 언리얼 엔진 프로젝트 이름 변경
ㄴ uproject 파일명 변경
ㄴ DefaultGame 의 /Script/EngineSettings.GeneralProjectSettings 섹션의 ProjectName 값 변경
ㄴ DefaultEngine 의 URL 섹션의 GameName 값 변경

2. 모듈 이름 변경
ㄴ모듈 폴더 이름 변경
ㄴ Target.cs 의 ExtraModuleNames 모듈 이름 변경
ㄴ Build.cs 의 DependencyModuleNames의 모듈 이름 변경
ㄴ 모듈 내  `프로젝트 이름_API`  변경
ㄴ IMPLEMENT_MODULE와 IMPLEMENT_PRIMARY_GAME_MODULE 같은 함수에서 사용하는 프로젝트 이름 변경

<h3>TODO</h3>
3. 플러그인 이름 변경
4. 타겟 이름 변경
5. C++ 클래스 이름 변경
6. 수정 전 백업 기능 추가
7. 작동 실패 시 되돌리기
