@echo off
REM parent directory EVi
set BASE_DIR=%~dp0EVi

REM run main.py
python "%BASE_DIR%\main.py"

REM run dbmeter.py
python "%BASE_DIR%\dbmeter\dbmeter.py"

pause