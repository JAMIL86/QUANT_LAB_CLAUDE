@echo off
title Chimera Quant Terminal - Iniciando

echo ============================================================
echo  Iniciando Chimera Quant Terminal
echo ============================================================
echo.

REM Navegar para o diretório do script
cd /d "%~dp0"

REM Iniciar o servidor em background (silencioso)
start "" python main.py

REM Aguardar o servidor subir
echo Aguardando servidor iniciar...
timeout /t 3 /nobreak >nul

REM Abrir no navegador
echo Abrindo navegador...
start "" http://localhost:8080

echo.
echo ============================================================
echo  Sistema iniciado com sucesso!
echo  Acesse: http://localhost:8080
echo ============================================================
echo.
echo Mantenha esta janela aberta enquanto o servidor estiver ativo.
echo Feche-a apenas quando quiser parar o sistema.
echo.
pause