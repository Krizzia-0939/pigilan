@echo off
setlocal
cd /d "%~dp0"

set "VENV_PY=%~dp0.venv\Scripts\python.exe"

if exist "%VENV_PY%" (
    "%VENV_PY%" -c "import tensorflow as tf" >nul 2>&1
    if not errorlevel 1 (
        "%VENV_PY%" -m streamlit run app.py
        goto :eof
    )
    echo The local .venv TensorFlow install could not load. Falling back to system Python...
)

python -m streamlit run app.py
