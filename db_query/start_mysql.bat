@echo off
REM Database Query Tool - MySQL Startup Script

echo ========================================
echo Database Query Tool - Startup
echo ========================================
echo.

echo Starting MySQL Server...
start "" /B "C:\Program Files\MySQL\MySQL Server 8.4\bin\mysqld.exe"
echo MySQL Server starting...
timeout /t 3 /nobreak > nul
echo.

echo MySQL Server is ready!
echo.
echo MySQL Connection Details:
echo   Host: localhost
echo   Port: 3306
echo   User: root
echo   Password: 123456
echo   Database: db_query
echo.
echo Project Configuration:
echo   .env file configured for MySQL
echo.
echo To start the backend server, run:
echo   cd backend
echo   powershell -ExecutionPolicy ByPass -c "& 'C:\Users\Administrator\.local\bin\uv.exe' run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo.
echo To start the frontend server, run:
echo   cd frontend
echo   powershell -ExecutionPolicy ByPass -c "& 'C:\Program Files\nodejs\npm.cmd' run dev"
echo.
echo MySQL is running in background. Close this window to stop MySQL.
echo.
pause