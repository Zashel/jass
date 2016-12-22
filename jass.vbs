'Dim exit_val
'exit_val = 1
'Do While exit_val = 1
'    texto = "Indica tu contrase" & Chr(241) & "a"
'    titulo = "Indica, por favor, tu contrase" & Chr(241) & "a de inicio de sesi" & Chr(243) & "n de windows"
'    pass = InputBox(titulo, texto)
'    exit_val = CreateObject("WScript.Shell").Run("update.cmd " & pass, 1, True)
'Loop
exit_val = CreateObject("WScript.Shell").Run("update.cmd " & pass, 1, True)
CreateObject("Wscript.Shell").Run "jass.cmd", 0, False