import Unreal as Unreal 
import os

def test_pattern():
    current_file_path = os.path.dirname(os.path.abspath(__file__))
    Unreal.proccess_module(current_file_path + r'\TestCase\LyraClient.Target.cs', "LyraGame", "KraverGame")
    
    Unreal.proccess_module(current_file_path + r'\TestCase\LyraEditor.cpp', "LyraGame", "KraverGame")
    Unreal.proccess_module(current_file_path + r'\TestCase\LyraEditor.Build.cs', "LyraGame", "KraverGame")
    Unreal.proccess_module(current_file_path + r'\TestCase\LyraGame.Build.cs', "LyraGame", "KraverGame")
    
    Unreal.proccess_module(current_file_path + r'\TestCase\LyraGameModule.cpp', "LyraGame", "KraverGame")

#test_pattern()
