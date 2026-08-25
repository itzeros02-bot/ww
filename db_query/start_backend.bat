@echo off
REM Backend Startup Script

cd "%~dp0backend"

echo ========================================
echo Database Query Tool - Backend
echo ========================================
echo.
echo Starting FastAPI development server...
echo Backend will be available at: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.

powershell -ExecutionPolicy ByPass -c "& 'C:\Users\Administrator\.local\bin\uv.exe' run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

pause