@echo off
title SentimentPulse - 24/7 Live Deployment
cd /d "%~dp0"
echo =====================================================================
echo    SENTIMENTPULSE - LIVE PUBLIC DEPLOYMENT & TUNNEL LAUNCHER
echo =====================================================================
echo.
echo [1/2] Verifying FastAPI Server on port 8000...
start /b py run.py

timeout /t 3 /nobreak >nul

echo [2/2] Starting Cloudflare Global Edge Tunnel...
echo.
echo Your public live URL will appear below:
echo =====================================================================
.\cloudflared.exe tunnel --url http://127.0.0.1:8000
pause
