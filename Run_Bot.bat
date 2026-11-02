@echo off
title Conquer Bot Launcher
color 0A

:: ---------------------------------------------------------
:: Check if the script is running as Administrator
:: ---------------------------------------------------------
net session >nul 2>&1
if %errorLevel% == 0 (
    goto :run_bot
) else (
    echo Requesting Administrator privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

:run_bot
:: ---------------------------------------------------------
:: Set the path to your project folder
:: ---------------------------------------------------------
cd /d "d:\Programming\Tools\Conquer_bot"

echo ==================================================
echo Starting Conquer Bot...
echo ==================================================
echo.

:: Run the python executable from your virtual environment
:: The -u flag forces the terminal to show prints immediately
".venv\Scripts\python.exe" -u "src\main.py"

:: If the bot crashes or stops, keep the window open so you can read the error
echo.
echo ==================================================
echo Bot stopped or crashed. 
echo Press any key to close this window.
echo ==================================================
pause >nul