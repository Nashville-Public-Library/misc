:: This will launch the python script.
:: WireReady cannot run .py files, so a batch file is needed to do it.
:: WireReady will run the batch file which runs the python file.

:: turn echo off
@echo off
echo Sending metadata...
echo.

:: change to current directory (directory of batch file)
CD /d "%~dp0"

:: run python script with command line argument
py %CD%\metadata.py --title "Name of some TL Show"