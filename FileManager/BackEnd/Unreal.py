import os
import sys
    
import Config as Config
import File as File
import Pattern as Pattern

def get_project_path(uproject_path):
    return os.path.dirname(uproject_path)

def proccess_module(file_path):
    if not os.path.isfile(file_path):
        print(f"파일을 찾을 수 없습니다: {file_path}")
        sys.exit(1)

    patterns = None;
    # 파일 확장자에 따라 패턴 설정
    if file_path.endswith('.cpp'):
        patterns = [
            Pattern.PatternInfo(
                search=r'(IMPLEMENT_PRIMARY_GAME_MODULE\s*\()\s*([^\)]*{old_name}[^\)]*)\)',
                item_name='IMPLEMENT_PRIMARY_GAME_MODULE',
                old_name='LyraGame',    # 변경 전 이름
                new_name='NewGameModule',    # 변경 후 이름
                args_to_check=[1, 2]
            ),
            Pattern.PatternInfo(
                search=r'(IMPLEMENT_MODULE\s*\()\s*([^\)]*{old_name}[^\)]*)\)',
                item_name='IMPLEMENT_MODULE',
                old_name='LyraEditor',
                new_name='NewModule',
                args_to_check=[1]
            )
        ]
    elif file_path.endswith('.cs'):
        patterns = [
            Pattern.PatternInfo(
                # ExtraModuleNames.AddRange 패턴 추가
                search=r'(ExtraModuleNames\.AddRange\s*\(\s*new\s+string\s*\[\]\s*\{{\s*([^\}}]*?)\s*\}}\s*\)\s*;)',
                item_name='ExtraModuleNames',
                old_name='LyraGame',
                new_name='NewModule',
            ),
            Pattern.PatternInfo(
                search=r'((?:Public|Private|)DependencyModuleNames\.AddRange\s*\(\s*new\s+string\s*\[\]\s*\{{\s*([^\}}]*{old_name}[^\}}]*)\s*\}}\s*\)\s*;)',
                item_name='DependencyModuleNames',
                old_name='LyraGame',
                new_name='NewDependency',
            ),
        ]

    Pattern.parse_Pattern(file_path, patterns)
    return file_path

def rename_project_name(uproject_path, new_name):
    # uproject 이름 변경
    File.Utility.rename_file(uproject_path, new_name)
    
    # Config 변경
    project_path = get_project_path(uproject_path)
    Config.parse_config(project_path + r"\Config\DefaultGame.ini", "/Script/EngineSettings.GeneralProjectSettings", "ProjectName", new_name)
    Config.parse_config(project_path + r"\Config\DefaultEngine.ini", "URL", "GameName", new_name)
    
def rename_module_name(uproject_path, target_name, new_name):
    project_path = get_project_path(uproject_path)
        
    File.parse_files_and_folders(project_path, proccess_module, None)
    
    