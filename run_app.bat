@echo off
setlocal
cd /d "%~dp0"

set "VENV_PY=%~dp0.venv\Scripts\python.exe"
set "PYTHON_CMD="
set "STREAMLIT_ARGS=app.py --server.headless true"

if exist "%VENV_PY%" set "PYTHON_CMD=%VENV_PY%"

if not defined PYTHON_CMD (
    py -3.11 -c "import sys" >nul 2>&1
    if not errorlevel 1 set "PYTHON_CMD=py -3.11"
)

if not defined PYTHON_CMD (
    py -3 -c "import sys" >nul 2>&1
    if not errorlevel 1 set "PYTHON_CMD=py -3"
)

if not defined PYTHON_CMD (
    python -c "import sys" >nul 2>&1
    if not errorlevel 1 set "PYTHON_CMD=python"
)

if not defined PYTHON_CMD (
    echo Pigilan could not find a working Python installation.
    echo.
    echo Install Python 3.11, then run:
    echo   py -3.11 -m venv .venv
    echo   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

%PYTHON_CMD% -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo Python was found, but Streamlit is not installed in that runtime.
    echo.
    echo Create the local environment and install dependencies:
    echo   py -3.11 -m venv .venv
    echo   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo Starting Pigilan with %PYTHON_CMD%...
%PYTHON_CMD% -m streamlit run %STREAMLIT_ARGS%
