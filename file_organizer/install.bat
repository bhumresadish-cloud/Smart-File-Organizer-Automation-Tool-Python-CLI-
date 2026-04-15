@echo off
REM Installation script for Smart File Organizer (Windows)

echo Installing Smart File Organizer...
echo.

REM Check Python version
echo Checking Python version...
python --version
echo.

REM Create virtual environment (optional)
set /p venv="Create virtual environment? (y/n): "
if /i "%venv%"=="y" (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo Virtual environment activated
    echo.
)

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
echo.

REM Create logs directory
echo Creating logs directory...
if not exist logs mkdir logs
echo.

REM Run tests
set /p tests="Run tests to verify installation? (y/n): "
if /i "%tests%"=="y" (
    echo Running tests...
    pytest tests/ -v
    echo.
)

REM Test CLI
echo Testing CLI...
python main.py --help
echo.

echo Installation complete!
echo.
echo Quick start:
echo   python main.py organize ^<path^>
echo   python main.py --help
echo.
echo Documentation:
echo   README.md - Full documentation
echo   QUICKSTART.md - Quick start guide
echo   USAGE_EXAMPLES.md - Real-world examples
echo.

pause
