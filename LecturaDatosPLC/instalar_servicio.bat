@echo off
:: =============================================================
:: instalar_servicio.bat
:: Ejecutar como Administrador
:: =============================================================

SET CARPETA=C:\inetpub\wwwroot\AgroindugestorQA\Servicio\PLCService
SET PYTHON=C:\Python312\python.exe   & REM ← ajusta la ruta a tu Python

echo.
echo  ╔══════════════════════════════════════════╗
echo  ║   PLC Curvas Tueste — Instalador         ║
echo  ╚══════════════════════════════════════════╝
echo.

:: Crear carpeta destino y subcarpeta de logs
if not exist "%CARPETA%\logs" mkdir "%CARPETA%\logs"

:: Copiar archivos al destino
echo [1/4] Copiando archivos a %CARPETA% ...
copy /Y config.py        "%CARPETA%\"
copy /Y logger_setup.py  "%CARPETA%\"
copy /Y plc_types.py     "%CARPETA%\"
copy /Y plc_reader.py    "%CARPETA%\"
copy /Y sql_writer.py    "%CARPETA%\"
copy /Y plc_service.py   "%CARPETA%\"

:: Instalar dependencias
echo [2/4] Instalando dependencias Python ...
"%PYTHON%" -m pip install pymodbus pyodbc pywin32 --quiet

:: Registrar pywin32 como servicio
echo [3/4] Registrando pywin32 ...
"%PYTHON%" "%CARPETA%\Scripts\pywin32_postinstall.py" -install 2>nul

:: Instalar y arrancar el servicio Windows
echo [4/4] Instalando servicio Windows ...
cd /d "%CARPETA%"
"%PYTHON%" plc_service.py install
"%PYTHON%" plc_service.py start

echo.
echo  ✔ Servicio PLCCurvasTueste instalado e iniciado.
echo  Log en: %CARPETA%\logs\plc_curvas.log
echo.
pause
