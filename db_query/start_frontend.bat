@echo off
REM Frontend Startup Script

cd "%~dp0frontend"

echo ========================================
echo Database Query Tool - Frontend
echo ========================================
echo.
echo Starting Vite development server...
echo Frontend will be available at: http://localhost:5173
echo Backend API: http://localhost:8000
echo.

"C:\Program Files\nodejs\node.exe" "node_modules\vite\bin\vite.js"

pause