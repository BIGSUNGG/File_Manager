using IronPython.Hosting;
using IronPython.Runtime.Operations;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.Scripting.Hosting;
using static System.Net.Mime.MediaTypeNames;

namespace Services
{
    public class PythonProcess
    {         
        // Project
        public readonly string SolutionPath;
        public readonly string ProjectPath;

        // IronPython
        private readonly ScriptEngine _pyEngine;
                 
        private readonly ScriptSource _utilityScource;
        private readonly ScriptScope _utilityScope;
                 
        private readonly ScriptSource _fileScource;
        private readonly ScriptScope _fileScope;

        private readonly ScriptSource _unrealScource;
        private readonly ScriptScope _unrealScope;

        object _lock = new object();

        public PythonProcess()
        {
            string filePath = AppDomain.CurrentDomain.BaseDirectory;
            SolutionPath    = Path.GetFullPath(Path.Combine(filePath, @"..\..\..\..\..\.."));
            ProjectPath     = Path.GetFullPath(Path.Combine(filePath, @"..\..\..\..\..\..\.."));

            // IronPython
            _pyEngine = Python.CreateEngine();
            _utilityScope = _pyEngine.CreateScope();
            _fileScope = _pyEngine.CreateScope();
            _unrealScope = _pyEngine.CreateScope();

            // 파이썬 모듈 참고 경로 추가
            var paths = _pyEngine.GetSearchPaths();
            paths.Add(ProjectPath + @"\Python");
            paths.Add(ProjectPath + @"\Python\DLLs");
            paths.Add(ProjectPath + @"\Python\Lib");
            paths.Add(ProjectPath + @"\Python\Lib\site-packages");
            paths.Add(SolutionPath + @"\BackEnd");
            _pyEngine.SetSearchPaths(paths);

            // Source 불러오기
            _utilityScource = _pyEngine.CreateScriptSourceFromFile(SolutionPath + @"\BackEnd\Utility.py");
            _utilityScource.Execute(_utilityScope);

            _fileScource = _pyEngine.CreateScriptSourceFromFile(SolutionPath + @"\BackEnd\File.py");
            _fileScource.Execute(_fileScope);

            _unrealScource = _pyEngine.CreateScriptSourceFromFile(SolutionPath + @"\BackEnd\Unreal.py");
            _unrealScource.Execute(_unrealScope);           
        }

        public object StringToBytes(string str)
        {
            try
            {
                object result;
                var strToBytes = _utilityScope.GetVariable("string_to_bytes");
                result = strToBytes(str);
                return result;
            }
            catch (System.Exception ex)
            {
                return new object();
            }
        }

        async public Task FileReplaceAsync(string path, string oldStr, string newStr,
            bool changeFolderName = true, bool searchChildFolder = true, bool changeFileContent = true, bool changeFileName = true, bool searchChildFiles = true)
        {
            await Task.Run(() =>
            {
                lock (_lock)
                {
                    try
                    {
                        var fileReplace = _fileScope.GetVariable("process_files_and_folders");
                        fileReplace(path, StringToBytes(oldStr), StringToBytes(newStr), changeFolderName, searchChildFolder, changeFileContent, changeFileName, searchChildFiles);
                    }
                    catch (System.Exception ex)
                    {

                    }
                }
            });
        }

        async public Task RenameProjectNameAsync(string projectPath, string targetName)
        {
            await Task.Run(() =>
            {
                lock (_lock)
                {
                    try
                    {
                        var renameProjectName = _unrealScope.GetVariable("rename_project_name");
                        renameProjectName(projectPath, targetName);
                    }
                    catch (System.Exception ex)
                    {

                    }
                }
            });
        }
    }
}
