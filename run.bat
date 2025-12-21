@echo off
REM ===================================================================
REM Roblox Account Creator Launcher
REM Automatically installs dependencies and runs the application
REM ===================================================================

title Roblox Account Creator - Launcher
color 0B

echo.
echo ================================================================
echo                ROBLOX ACCOUNT CREATOR LAUNCHER
echo ================================================================
echo.

REM Check if Python is installed
echo [*] Checking for Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] ERROR: Python is not installed or not in PATH
    echo [!] Please install Python 3.7 or higher from python.org
    echo.
    pause
    exit /b 1
)

REM Display Python version
for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo [+] Found: %PYTHON_VERSION%
echo.

REM Check if requirements.txt exists
if not exist "requirements.txt" (
    echo [!] ERROR: requirements.txt not found
    echo [!] Please ensure all files are in the correct directory
    echo.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv\" (
    echo [*] Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [!] ERROR: Failed to create virtual environment
        echo [!] Trying to continue without virtual environment...
        goto :install_deps
    )
    echo [+] Virtual environment created successfully
    echo.
)

REM Activate virtual environment
echo [*] Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [!] WARNING: Could not activate virtual environment
    echo [!] Continuing with system Python...
)

:install_deps
REM Install/Update dependencies
echo [*] Installing/Updating dependencies...
echo [*] This may take a few minutes on first run...
echo.
python -m pip install --upgrade pip --quiet

REM Install packages individually for better Windows compatibility
echo [*] Installing requests...
python -m pip install "requests>=2.31.0" --quiet
echo [*] Installing pillow...
python -m pip install "pillow>=10.0.0" --quiet
echo [*] Installing numpy...
python -m pip install "numpy>=1.24.0,<2.0.0" --quiet
echo [*] Installing opencv-python...
python -m pip install "opencv-python>=4.8.0,<5.0.0" --quiet
echo [*] Installing colorama...
python -m pip install "colorama>=0.4.6" --quiet

if %errorlevel% neq 0 (
    echo [!] ERROR: Failed to install dependencies
    echo [!] If you see compiler errors, try:
    echo [!]   1. Close this window
    echo [!]   2. Open Command Prompt as Administrator
    echo [!]   3. Run: python -m pip install --upgrade pip
    echo [!]   4. Run this launcher again
    echo.
    pause
    exit /b 1
)

echo [+] Dependencies installed successfully
echo.

REM Check if required Python files exist
echo [*] Verifying required files...
set MISSING_FILES=0

if not exist "main.py" (
    echo [!] ERROR: main.py not found
    set MISSING_FILES=1
)
if not exist "roblox_signup.py" (
    echo [!] ERROR: roblox_signup.py not found
    set MISSING_FILES=1
)
if not exist "funcaptcha_solver.py" (
    echo [!] ERROR: funcaptcha_solver.py not found
    set MISSING_FILES=1
)
if not exist "funcaptcha_utils.py" (
    echo [!] ERROR: funcaptcha_utils.py not found
    set MISSING_FILES=1
)
if not exist "generate.py" (
    echo [!] ERROR: generate.py not found
    set MISSING_FILES=1
)
if not exist "generate_counter.py" (
    echo [!] ERROR: generate_counter.py not found
    set MISSING_FILES=1
)
if not exist "util.py" (
    echo [!] ERROR: util.py not found
    set MISSING_FILES=1
)

if %MISSING_FILES% equ 1 (
    echo [!] ERROR: Some required files are missing
    echo.
    pause
    exit /b 1
)

echo [+] All required files present
echo.

REM Create accounts.txt if it doesn't exist
if not exist "accounts.txt" (
    echo [*] Creating accounts.txt file...
    type nul > accounts.txt
)

REM Display startup message
echo ================================================================
echo                    STARTING APPLICATION
echo ================================================================
echo.
timeout /t 2 /nobreak >nul

REM Run the main application with threading
python main.py

REM Check if the program exited with an error
if %errorlevel% neq 0 (
    echo.
    echo ================================================================
    echo [!] Application exited with an error
    echo ================================================================
    echo.
    pause
    exit /b %errorlevel%
)

REM Deactivate virtual environment if it was activated
if defined VIRTUAL_ENV (
    call venv\Scripts\deactivate.bat
)

echo.
echo ================================================================
echo                   APPLICATION CLOSED
echo ================================================================
echo.
pause
