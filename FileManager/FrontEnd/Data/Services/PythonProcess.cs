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
        public readonly string solutionPath;
        public readonly string projectPath;

        // IronPython
        private readonly ScriptEngine pyEngine;

        private readonly ScriptSource utilityScource;
        private readonly ScriptScope utilityScope;

        private readonly ScriptSource replaceScource;
        private readonly ScriptScope replaceScope;

        public PythonProcess()
        {
            string filePath = AppDomain.CurrentDomain.BaseDirectory;
            solutionPath    = Path.GetFullPath(Path.Combine(filePath, @"..\..\..\..\..\.."));
            projectPath     = Path.GetFullPath(Path.Combine(filePath, @"..\..\..\..\..\..\.."));

            // IronPython
            pyEngine = Python.CreateEngine();
            utilityScope = pyEngine.CreateScope();
            replaceScope = pyEngine.CreateScope();

            // 파이썬 모듈 참고 경로 추가
            var paths = pyEngine.GetSearchPaths();
            paths.Add(projectPath + @"\Python");
            paths.Add(projectPath + @"\Python\DLLs");
            paths.Add(projectPath + @"\Python\Lib");
            paths.Add(projectPath + @"\Python\Lib\site-packages");
            pyEngine.SetSearchPaths(paths);

            // Source 불러오기
            utilityScource = pyEngine.CreateScriptSourceFromFile(solutionPath + @"\BackEnd\Utility.py");
            utilityScource.Execute(utilityScope);

            replaceScource = pyEngine.CreateScriptSourceFromFile(solutionPath + @"\BackEnd\FileReplace.py");
            replaceScource.Execute(replaceScope);
        }

        public object StringToBytes(string str)
        {
            try
            {
                object result;
                var strToBytes = utilityScope.GetVariable("string_to_bytes");
                result = strToBytes(str);
                return result;
            }
            catch (System.Exception ex)
            {
                return new object();
            }
        }

        public void FileReplace(string path, string oldStr, string newStr)
        {
            try
            {
                var fileReplace = replaceScope.GetVariable("process_files_and_folders");
                fileReplace(path, StringToBytes(oldStr), StringToBytes(newStr));
            }
            catch (System.Exception ex)
            {

            }
        }
    }
}
