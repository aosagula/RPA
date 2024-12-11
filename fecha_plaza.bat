rem @echo off
call %HOMEDRIVE%%HOMEPATH%\Anaconda3\Scripts\activate.bat RPA 


python %HOMEDRIVE%%HOMEPATH%\RPA\varios\fecha_plaza.py> %TEMP%\fecha_plaza.log 2>&1


