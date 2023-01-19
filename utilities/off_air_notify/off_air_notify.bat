@echo off
SETLOCAL DisableDelayedExpansion

:: change to current directory (directory of batch file)
CD /d "%~dp0"

:: capture command line argument from syslog server
set something=%1

:: run python script with command line argument
off_air_notify.py --feed_name %something%