@echo off

set PYTHONHOME=C:\Program Files\ArcGIS\Server\framework\runtime\ArcGIS\bin\Python\envs\arcgispro-py3-scripts
set OUTPUT_FOLDER=E:\data\inputs\ZipCodeScraper

set SCRIPTSHOME=%~dp0
set LOG_LEVEL=DEBUG
set LOGHOME=%SCRIPTSHOME%\logging
set TEMP_OUTPUT_FOLDER=%SCRIPTSHOME%\output

set LOGFILE=%LOGHOME%\ZipCodeScraper.log

echo Running Zip Code Scraper
"%PYTHONHOME%\python.exe" "%SCRIPTSHOME%\main.py" "%TEMP_OUTPUT_FOLDER%" > "%LOGFILE%" 2>&1

echo Copying Zip Code CSV Files to Output Folder
copy "%TEMP_OUTPUT_FOLDER%\*.csv" "%OUTPUT_FOLDER%" >> "%LOGFILE%" 2>&1

echo Deleting Zip Code CSV Files in Temporary Output Folder
del /q "%TEMP_OUTPUT_FOLDER%\*.csv" >> "%LOGFILE%" 2>&1

