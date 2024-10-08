import Config
import File
import os

def get_project_path(uproject_path):
    return os.path.dirname(uproject_path)

def rename_project_name(uproject_path, new_name):
    # uproject 이름 변경
    File.rename_file(uproject_path, new_name)
    
    # Config 변경
    project_path = get_project_path(uproject_path)
    Config.update_config_value(project_path + r"\Config\DefaultGame.ini", "/Script/EngineSettings.GeneralProjectSettings", "ProjectName", new_name)
    Config.update_config_value(project_path + r"\Config\DefaultEngine.ini", "URL", "GameName", new_name)
    
def rename_module_name(uproject_path, target_name, new_name):
        