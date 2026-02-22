@echo off
REM ZeroTrace Quick Setup Script for Windows

echo ================================================
echo     ZeroTrace Setup
echo ================================================
echo.

REM Check Python version
echo Checking Python version...
python --version
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.8 or higher.
    pause
    exit /b 1
)
echo [OK] Python found
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] Dependencies installed
echo.

REM Check if Ollama is installed
echo Checking for Ollama...
where ollama >nul 2>nul
if %errorlevel% equ 0 (
    echo [OK] Ollama found
    
    REM Check if llama3 is available
    ollama list | findstr /C:"llama3" >nul
    if errorlevel 1 (
        echo [WARNING] Llama3 model not found. Installing...
        ollama pull llama3
    ) else (
        echo [OK] Llama3 model found
    )
) else (
    echo [WARNING] Ollama not found. AI action plans will not be available.
    echo            Install Ollama from: https://ollama.ai/
)

echo.
echo ================================================
echo     Setup Complete!
echo ================================================
echo.
echo To start ZeroTrace, run:
echo   streamlit run app.py
echo.
echo Sample data available:
echo   - CVE database: data\sample_cves.json (21 CVEs)
echo   - Asset inventory: data\sample_assets.csv (15 assets)
echo.
pause
