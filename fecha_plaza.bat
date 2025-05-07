rem @echo off
call %HOMEDRIVE%%HOMEPATH%\Anaconda3\Scripts\activate.bat RPA 

FOR /F "tokens=*" %%A IN ('DATE/T') DO FOR %%B IN (%%A) DO SET Today=%%B

FOR /F "tokens=1-3 delims=/-" %%A IN ("%Today%") DO (
    SET Dia=%%A
    SET Mes=%%B
    SET Anio=%%C
)

SET FILENAMELOG=%Anio%-%Mes%-%Dia%
print %FILENAMELOG% 2>&1
%HOMEDRIVE%%HOMEPATH%\Anaconda3\envs\RPA\python.exe %HOMEDRIVE%%HOMEPATH%\RPA\varios\fecha_plaza.py>> %TEMP%\fecha_plaza_%FILENAMELOG%.log 2>&1

