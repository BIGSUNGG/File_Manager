from ast import Lambda
import os
import sys
    
from Parse import Config
from Parse import File
from Parse import Pattern
from Utility import ContentUtility
from Utility import FileUtility
from FileHandler import FileHandler

def rename_project_name(uproject_path, new_name):
    project_path = FileUtility.get_base_path(uproject_path)
    
    # uproject
    uproject_handler = FileHandler(uproject_path)
    uproject_handler.read_file()
    uproject_handler.action_path(lambda path : FileUtility.rename_file(path, '{0}.uproject'.format(new_name)))
    uproject_handler.write_file() 
    
    # Config 변경
    # DefaultGame Config 변경
    default_game_handler = FileHandler(project_path + r"\Config\DefaultGame.ini")
    default_game_handler.read_file()
    default_game_handler.action_content(lambda content : Config.parse_config(content, "/Script/EngineSettings.GeneralProjectSettings", "ProjectName", new_name))        
    default_game_handler.write_file()

    # DefaultEngine Config 변경
    project_path = FileUtility.get_base_path(uproject_path)
    default_engine_handler = FileHandler(project_path + r"\Config\DefaultEngine.ini")
    default_engine_handler.read_file()
    default_engine_handler.action_content(lambda content : Config.parse_config(content,  "URL", "GameName", new_name))        
    default_engine_handler.write_file()
    
def rename_module_name(uproject_path, old_name, new_name):
    project_path = FileUtility.get_base_path(uproject_path)
    
    # uproject
    uproject_handler = FileHandler(uproject_path)
    uproject_handler.read_file()
    
    uproject_patterns = [    
        Pattern.PatternInfo(
        search=r'("Modules"\s*:\s*\[\s*(?:\{[^}]*?\}\s*,\s*)*)("Name"\s*:\s*)"LyraGame"',
        item_name='Modules',
        old_name = old_name,
        new_name = new_name
    )]      
    
    uproject_handler.action_content(lambda content : Pattern.parse_pattern(content, uproject_patterns))
    uproject_handler.write_file() 
    
    # module folder
    module_folder_handler = FileHandler(project_path + r'\Source\{0}'.format(old_name))
    module_folder_handler.read_file()
    module_folder_handler.action_path(lambda path : ContentUtility.rename_file(path, new_name))
    module_folder_handler.write_file() 
    
    # config
    File.parse_files_and_folders(project_path + r'\Config', lambda path : proccess_module(path, old_name, new_name), None)
    
    # source
    File.parse_files_and_folders(project_path + r'\Source', lambda path : proccess_module(path, old_name, new_name), None)
    
def proccess_module(file_path, old_module_name, new_module_name):
    handler = FileHandler(file_path)
    handler.read_file()

    # 파일 확장자에 따라 패턴 설정
    if file_path.endswith('.cpp'):        
        patterns = [
            Pattern.PatternInfo(
                search=r'(?P<before>IMPLEMENT_MODULE\s*\(\s*)(?P<args>[^\)]+)\s*\)',
                item_name='IMPLEMENT_MODULE',
                old_name=old_module_name,
                new_name=new_module_name,
                args_to_check=[1]  # 두 번째 인자 (인덱스 1)만 검사
            ),
            Pattern.PatternInfo(
                search=r'(?P<before>IMPLEMENT_PRIMARY_GAME_MODULE\s*\(\s*)(?P<args>[^\)]+)\s*\)',
                item_name='IMPLEMENT_PRIMARY_GAME_MODULE',
                old_name=old_module_name,
                new_name=new_module_name,
                args_to_check=[1, 2]  # 두 번째 및 세 번째 인자 (인덱스 1, 2) 검사
            )
        ]
        handler.action_content(lambda content : Pattern.parse_pattern(content, patterns))        
        handler.action_content(lambda content : ContentUtility.change_keyword(content, '{0}_API'.format(old_module_name.upper()), '{0}_API'.format(new_module_name.upper())))        
    elif file_path.endswith('.Target.cs'):
        patterns = [
            Pattern.PatternInfo(
                search=r'(?P<before>\bExtraModuleNames\.AddRange\s*\(\s*new\s+string\[\]\s*\{{\s*)(?P<args>[^}}]+)(\s*\}}\s*\)\s*;)',
                item_name='ExtraModuleNames.AddRange',
                old_name=old_module_name,
                new_name=new_module_name,
                args_to_check=None  # 모든 인자 검사
            ),
        ]
        handler.action_content(lambda content : Pattern.parse_pattern(content, patterns))        
    elif file_path.endswith('.Build.cs'):
        patterns = [
            Pattern.PatternInfo(
                search=r'(?P<before>PublicIncludePaths\.AddRange\s*\(\s*new\s+string\[\]\s*\{{\s*)(?P<args>[^}}]+)(\s*\}}\s*\)\s*;)',
                item_name='PublicIncludePaths.AddRange',
                old_name=old_module_name,
                new_name=new_module_name,
                args_to_check=None  # 모든 인자 검사
            ),
            Pattern.PatternInfo(
                search=r'(?P<before>PrivateIncludePaths\.AddRange\s*\(\s*new\s+string\[\]\s*\{{\s*)(?P<args>[^}}]+)(\s*\}}\s*\)\s*;)',
                item_name='PrivateIncludePaths.AddRange',
                old_name=old_module_name,
                new_name=new_module_name,
                args_to_check=None  # 모든 인자 검사
            ),
            Pattern.PatternInfo(
                search=r'(?P<before>PublicDependencyModuleNames\.AddRange\s*\(\s*new\s+string\[\]\s*\{{\s*)(?P<args>[^}}]+)(\s*\}}\s*\)\s*;)',
                item_name='PublicDependencyModuleNames.AddRange',
                old_name=old_module_name,
                new_name=new_module_name,
                args_to_check=None  # 모든 인자 검사
            ),
            Pattern.PatternInfo(
                search=r'(?P<before>PrivateDependencyModuleNames\.AddRange\s*\(\s*new\s+string\[\]\s*\{{\s*)(?P<args>[^}}]+)(\s*\}}\s*\)\s*;)',
                item_name='PrivateDependencyModuleNames.AddRange',
                old_name=old_module_name,
                new_name=new_module_name,
                args_to_check=None  # 모든 인자 검사
            ),
        ]
        handler.action_content(lambda content : Pattern.parse_pattern(content, patterns))        
        if file_path.endswith('{0}.Build.cs'.format(old_module_name)):
            handler.action_path(lambda path : FileUtility.rename_file(path, '{0}.Build.cs'.format(new_module_name)))                
    elif file_path.endswith('.ini'):
        handler.action_content(lambda content : ContentUtility.change_keyword(content, old_module_name + r'.', new_module_name + r'.'))
        if file_path.endswith('DefaultEngine.ini'):
            handler.action_content(lambda content : Config.parse_config(content, "CoreRedirects", "PackageRedirects", '(OldName="/Script/{0}",NewName="/Script/{1}")'.format(old_module_name, new_module_name), True))        

    handler.write_file()

    return handler.file_path
