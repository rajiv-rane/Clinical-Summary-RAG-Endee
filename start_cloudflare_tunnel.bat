@echo off
REM Quick Cloudflare Tunnel Starter for RAG App
REM This script starts a quick tunnel for your Streamlit app

echo ============================================================
echo   Cloudflare Tunnel - Quick Start
echo ============================================================
echo.

REM Check if cloudflared is installed
where cloudflared >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] cloudflared is not installed or not in PATH
    echo.
    echo Please install cloudflared first:
    echo   1. Download from: https://github.com/cloudflare/cloudflared/releases
    echo   2. Or run: choco install cloudflared
    echo   3. Or see CLOUDFLARE_TUNNEL_SETUP.md for detailed instructions
    echo.
    pause
    exit /b 1
)

echo [INFO] Starting Cloudflare Tunnel for Streamlit (port 8501)...
echo [INFO] Your app will be accessible via the URL shown below
echo [INFO] Press Ctrl+C to stop the tunnel
echo.
echo ============================================================
echo.

REM Start the tunnel
cloudflared tunnel --url http://localhost:8501

pause
