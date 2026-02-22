@echo off
REM Quick run script for ZeroTrace

echo ================================================
echo     Starting ZeroTrace
echo ================================================
echo.

REM Check if in correct directory
if not exist "app.py" (
    echo [ERROR] Please run this script from the zerotrace directory
    pause
    exit /b 1
)

REM Check if dependencies are installed
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo [WARNING] Dependencies not installed. Running setup...
    pip install -r requirements.txt
)

REM Check Ollama
where ollama >nul 2>nul
if %errorlevel% equ 0 (
    ollama list 2>nul | findstr /C:"llama3" >nul
    if errorlevel 1 (
        echo [WARNING] llama3 model not found. AI action plans unavailable.
        echo            Run: ollama pull llama3
    ) else (
        echo [OK] Ollama with llama3 is ready
    )
) else (
    echo [INFO] Ollama not found. AI action plans will be unavailable.
)

echo.
echo ================================================
echo     Launching ZeroTrace...
echo ================================================
echo.
echo Sample data available:
echo   - CVE Database: data\sample_cves.json
echo   - Asset Inventory: data\sample_assets.csv
echo.
echo Press Ctrl+C to stop
echo.

streamlit run app.py
