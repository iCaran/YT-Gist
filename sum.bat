@echo off
setlocal enabledelayedexpansion

:loop
set /p url=Enter URL (or press Enter to exit): 
if "!url!" == "" (
    exit /b
) else (
    python main.py -u "!url!"
)
goto loop
