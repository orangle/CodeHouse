@echo on
color 2f
mode con: cols=80 lines=25
@REM
@echo start to clean all .py files in current directory and children directories
@rem for /r . %%a in (.) do @if exist "%%a\*.py" @echo "%%a\*.py"
@for /r . %%a in (.) do @if exist "%%a\*.py" del /a /f /s "%%a\*.py"
@echo «Â¿ÌÕÍ±œ£°
@pause
