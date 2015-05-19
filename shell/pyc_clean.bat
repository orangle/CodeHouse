@echo on
color 2f
mode con: cols=80 lines=25
@REM
@echo start to clean all .pyc files in current directory and children directories
@rem for /r . %%a in (.) do @if exist "%%a\*.pyc" @echo "%%a\*.pyc"
@for /r . %%a in (.) do @if exist "%%a\*.pyc" del /a /f /s "%%a\*.pyc"
@echo clean up...
@pause
