@echo off
chcp 65001 > nul
echo =====================================
echo   Deploy Rápido - Olhar Literário
echo =====================================
echo.

set /p mensagem="Digite a mensagem do commit (ou Enter para usar padrão): "

if "%mensagem%"=="" (
    set mensagem=Atualização automática
)

echo.
echo Executando deploy...
echo.

powershell.exe -ExecutionPolicy Bypass -File "%~dp0deploy.ps1" -mensagem "%mensagem%"

echo.
pause
