@echo off
REM Blockline - venv setup (Windows)
REM
REM Usage:
REM   setup_venv.bat
REM
REM Then activate with:
REM   venv\Scripts\activate

echo ============================================================
echo  Blockline - Setting up virtual environment (Windows)
echo ============================================================

where python >nul 2>nul
if errorlevel 1 (
    echo Python not found on PATH. Install Python 3.10+ from python.org
    exit /b 1
)

if not exist venv (
    echo Creating venv...
    python -m venv venv
) else (
    echo venv already exists, reusing it.
)

call venv\Scripts\activate.bat

echo Upgrading pip...
python -m pip install --upgrade pip >nul

if exist requirements.txt (
    echo Installing requirements.txt ...
    pip install -r requirements.txt
) else (
    echo requirements.txt not found - skipping.
)

echo.
echo ============================================================
echo  Done. Activate the environment with:
echo    venv\Scripts\activate
echo  Then run the app with:
echo    python main.py
echo ============================================================
