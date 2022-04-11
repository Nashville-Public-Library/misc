:: ----------
:: THIS SCRIPT USES FFMPEG TO CONVERT VARIOUS TYPES OF AUDIO FILES TO WAV FILES
:: IT WILL OUTPUT A MONO WAV FILE WITH A SAMPLE RATE OF 44,100 Hz
:: BIT DEPTH WILL BE UNCHANGED
::
:: IT CAN ALSO CONVERT WAV FILES TO WAV FILES...
:: ...WHICH MAY BE HELPFUL FOR OPENING "PROTECTED" OR OTHERWISE UNREADABLE WAV FILES.
::
:: PLEASE NOTE THIS WILL CONVERT *ALL* AUDIO FILES (OF THE SUPPORTED FORMATS)...
:: ...IN THE CURRENT DIRECTORY
:: 
:: WHEN COMPILING TO AN EXE FILE, MAKE SURE TO EMBED FFMPEG AND EXTRACT IT TO CURRENT DIRECTORY
:: ----------

:: TURN OFF ECHO
@echo off

:: THESE SETTINGS RELATE TO LOCAL VARIABLES
SETLOCAL EnableDelayedExpansion

:: HIDE FFMPEG. THIS IS NOT NEEDED IN BATCH... 
:: ...ONLY NEDED WHEN COMPILING TO AN EXE FILE!
::attrib +h %cd%\ffmpeg.exe

:: STORE OUR SUPPORTED FORMATS IN VARIABLES
set supported_format1=MP3
set supported_format2=M4A
set supported_format3=WAV
set supported_format4=FLAC

:start
cls
:: DISPLAY SOME TEXT AND ASK IF THE USER IS SURE
echo --------------------CONVERT--------------------
echo.
echo This will convert the audio files in %cd% to WAV files
echo.
echo Supported input formats are: %supported_format1%, %supported_format2%, %supported_format3%, %supported_format4%
echo.
Echo Are you sure you want to convert the audio files in %cd%?
echo.
echo --------------------
echo.
set /p question=(Type yes or y for yes, or anything else for no)
set answer=%question%
cls

:: IF USER ANSWERS YES TO ABOVE PROMPT, CONTINUE
:: IF NOT, GO TO END OF FILE AND DISPLAY MESSAGE
if /I %answer%==yes (goto sf0) else (goto next)
:next
if /I %answer%==y (goto sf0) else (goto nofile)

:: CHECK WHETHER THERE ARE ANY SUPPORTED AUDIO FILES IN THE CURRENT DIRECTORY
:: !CD! is for current directory. * is a wildcard.
:: IF YES, CONTINUE. IF NOT, GO TO END OF FILE AND DISPLAY MESSAGE
:sf0
if NOT exist !CD!\*.%supported_format1% (goto sf1) else (goto begin_convert) 
:sf1
if NOT exist !CD!\*.%supported_format2% (goto sf2) else (goto begin_convert)
:sf2
if NOT exist !CD!\*.%supported_format3% (goto sf3) else (goto begin_convert)
:sf3
if NOT exist !CD!\*.%supported_format4% (goto sf4) else (goto begin_convert)
:sf4
goto sfend

:: NOW WE CAN START CONVERTING THE FILE(S)
:begin_convert
:: WE START WITH THE WAV FILE(S)
cls
echo working on it...
:: FIRST WE WILL STORE THE ORIGINAL NAME OF THE FILE(S) IN A VARIABLE CALLED MYNAME
for %%G in (*.wav) do (
set MYNAME=%%~nxG
REM WE HAVE STORED THE ORIGINAL NAME. NOW GIVE THE FILE(S) A UNIFORM NAME FOR FFMPEG
ren !MYNAME! delete1.wav
REM USE FFMPEG TO CONVERT THE FILE(S)
ffmpeg -hide_banner -loglevel quiet -i !cd!\delete1.wav -ar 44100 -ac 1 !cd!\delete2.wav
REM DELETE THE ORIGINAL FILE
del delete1.wav
REM REPLACE THE NAME OF THE CONVERTED FILE WITH THE ORIGINAL NAME
ren delete2.wav !MYNAME!
REM CLOSE THE FOR LOOP WITH A BRACKET!
)
:: ----------

:: ----------
:: NOW WE MOVE ON TO THE MP3 FILE(S)
cls
echo working on it...
:: FIRST WE WILL STORE THE ORIGINAL NAME OF THE FILE(S) IN A VARIABLE CALLED MYNAME
for %%G in (*.mp3) do (
set MYNAME="%%~nxG"
REM THE NAME IS NOW STORED. NOW CHANGE THE ORIGINAL NAME TO A STANDARD NAME FOR FFMPEG
ren !MYNAME! delete1.mp3
REM USE FFMPEG TO CONVERT THE FILE
ffmpeg -hide_banner -loglevel quiet -i !cd!\delete1.mp3 -ar 44100 -ac 1 !cd!\delete2.wav
REM DELETE THE ORIGINAL FILE
del delete1.mp3
REM REPLACE THE NAME OF THE CONVERTED FILE WITH THE ORIGINAL NAME
ren delete2.wav !MYNAME!
REM THE FILE IS NOW A WAV FILE WITH THE ORIGINAL NAME, BUT THE .MP3 EXTENSION REMAINS.
REM TO AVOID CONFUSION, CHANGE IT.
ren !MYNAME! *.wav
)
:: ----------

:: ----------
:: NOW WE MOVE ON TO THE M4A FILE(S)
cls
echo working on it...
:: FIRST WE WILL STORE THE ORIGINAL NAME OF THE FILE(S) IN A VARIABLE CALLED MYNAME
for %%G in (*.m4a) do (
set MYNAME="%%~nxG"
REM THE NAME IS NOW STORED. NOW CHANGE THE ORIGINAL NAME TO A STANDARD NAME FOR FFMPEG
ren !MYNAME! delete1.m4a
REM USE FFMPEG TO CONVERT THE FILE
ffmpeg -hide_banner -loglevel quiet -i !cd!\delete1.m4a -ar 44100 -ac 1 !cd!\delete2.wav
REM DELETE THE ORIGINAL FILE
del delete1.m4a
REM REPLACE THE NAME OF THE CONVERTED FILE WITH THE ORIGINAL NAME
ren delete2.wav !MYNAME!
REM THE FILE IS NOW A WAV FILE WITH THE ORIGINAL NAME, BUT THE .M4A EXTENSION REMAINS.
REM TO AVOID CONFUSION, CHANGE IT.
ren !MYNAME! *.wav
)
:: ----------

:: ----------
:: NOW WE MOVE ON TO THE FLAC FILE(S)
cls
echo working on it...
:: FIRST WE WILL STORE THE ORIGINAL NAME OF THE FILE(S) IN A VARIABLE CALLED MYNAME
for %%G in (*.flac) do (
set MYNAME=%%~nxG
REM WE HAVE STORED THE ORIGINAL NAME. NOW GIVE THE FILE(S) A UNIFORM NAME FOR FFMPEG
ren !MYNAME! delete1.flac
REM USE FFMPEG TO CONVERT THE FILE(S)
ffmpeg -hide_banner -loglevel quiet -i !cd!\delete1.flac -ar 44100 -ac 1 !cd!\delete2.wav
REM DELETE THE ORIGINAL FILE
del delete1.flac
REM REPLACE THE NAME OF THE CONVERTED FILE WITH THE ORIGINAL NAME
ren delete2.wav !MYNAME!
REM THE FILE IS NOW A WAV FILE WITH THE ORIGINAL NAME, BUT THE .FLAC EXTENSION REMAINS.
REM TO AVOID CONFUSION, CHANGE IT.
ren !MYNAME! *.wav
REM CLOSE THE FOR LOOP WITH A BRACKET!
)

goto success

:: ----------

:nofile
echo You typed "%answer%", so nothing was converted
echo.
set /p question2=Type yes or y to start over, or anything else to quit: 
set answer2=%question2%
if /I %answer2%==yes (goto start) else (goto next2)
:next2
if /I %answer2%==y (goto start) else (goto end)
goto end

:: ----------

:success
cls
echo Your files are converted. Enjoy
echo.
echo (press any key to quit)
echo.
pause> nul
goto end

:: ----------

:sfend
echo I cannot find any %supported_format1%, %supported_format2%, %supported_format3%, or %supported_format4% files in %cd%. Sorry about that.
echo.
echo Do you want to try again?
echo.
set /p question3=Type yes or y to start over, or anything else to quit: 
set answer3=%question3%
if /I %answer3%==yes (goto start) else (goto next3)
:next3
if /I %answer3%==y (goto start) else (goto end)
goto end

:: ----------

:end

:: ----------
:: WRITTEN BY BEN WEDDLE
:: UPDATED 29 NOVEMBER 2021
:: ----------