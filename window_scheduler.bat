@echo off
echo Starting Docker Desktop...
start "" DOCKER_LOCATION

:CHECK_DOCKER
timeout /t 10 /nobreak
docker ps >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Waiting for Docker to be ready...
    goto CHECK_DOCKER
)

echo Docker is ready. Starting containers...
cd /d APP_LOCATION
docker-compose up -d
if %ERRORLEVEL% EQU 0 (
    echo %date% %time% - Successfully started container >> C:\Scripts\docker-startup.log
) else (
    echo %date% %time% - Failed to start container. Error code: %ERRORLEVEL% >> C:\Scripts\docker-startup.log
)

