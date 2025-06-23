@echo off
SETLOCAL ENABLEEXTENSIONS ENABLEDELAYEDEXPANSION

REM Obtener fecha
FOR /F "tokens=1-3 delims=/- " %%A IN ('DATE /T') DO (
    SET Dia=%%A
    SET Mes=%%B
    SET Anio=%%C
)
SET FILENAMELOG=!Anio!-!Mes!-!Dia!
SET LOGFILE=%TEMP%\fecha_plaza_!FILENAMELOG!.log

echo "Validar existencia de activate.bat" >> "!LOGFILE!"
IF NOT EXIST "C:\users\auto\Anaconda3\Scripts\activate.bat" (
    echo ERROR: No se encuentra activate.bat >> "!LOGFILE!"
    exit /b 1
)

echo Validar entorno de Python >> "!LOGFILE!"
IF NOT EXIST "C:\users\auto\Anaconda3\envs\RPA\python.exe" (
    echo ERROR: No se encuentra python.exe del entorno RPA >> "!LOGFILE!"
    exit /b 2
)

echo Validar script Python >> "!LOGFILE!"
IF NOT EXIST "C:\users\auto\RPA\varios\fecha_plaza.py" (
    echo ERROR: No se encuentra fecha_plaza.py >> "!LOGFILE!"
    exit /b 3
)

echo Activar entorno y ejecutar script >> "!LOGFILE!"
call "C:\users\auto\Anaconda3\Scripts\activate.bat" RPA >> "!LOGFILE!" 2>&1
"C:\users\auto\Anaconda3\envs\RPA\python.exe" "C:\users\auto\RPA\varios\fecha_plaza.py" >> "!LOGFILE!" 2>&1

ENDLOCAL
