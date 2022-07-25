# MISC 

### This repo contains MISC Python scripts to automate various tasks at the TL.

For *all* these scripts, you must have Python 3.10.1+ **AND Windows binaries for the following installed on the PC and added to the PATH**:
- [FFmpeg](https://www.ffmpeg.org) AND FFprobe
- [WGET](https://www.gnu.org/software/wget/)

Some scripts also use Twilio for notifications. There is a Twilio library for Python. It is not in the Python standard library and needs to be installed via PIP (`pip install twilio`). Store the Twilio credentials in environment variables on the PCs. The alternative is to use `curl` and long, complicated URLs.

### In fact, a number of variables used in these scripts are stored in environment variables. For example:
- syslog server
- mail server
- Twilio "to" and "from" numbers
- And more. Make sure to check all of them. 


### We run most of these scripts via WireReady (WR)
- The "Run" command in WR defaults to running from a different directory AND a different drive letter. This causes confusion.
- WR also does not run `.py` files by default. 
- For these reasons and more, we do not run `.py` files directly from WR.
- Instead, we tell WR to run a Batch script (`.bat` file) which in turn will run the Python script (`.py` file). 
- The batch script ensures we CD to the correct directory.
- Ensure the Batch & Python scripts are in the same directory.
- A sample `.bat` file (`Example.bat`) is inlcuded in this repo.

As a general note: It's best to avoid spaces in filenames. If your audio filenames have spaces in them, the FFmpeg commands will need to be changed.

### The scripts should be fairly straightfoward and self-explanatory but below are some helpful notes.

---

## AnimalAir.py

TL script to process Animal Airwaves (AA) each day.
- We are provided 12 episodes of AA per month. Download them at the beginning of each month from Content Depot.
- Place all 12 files in a local folder (delete last month's files)
- Since there are only 12 episodes, but we need to air it every day, we will usually need to air each episode more than once.
- The script will randomize which episode is used each day, ensuring the same episode never airs two days in a row.
- Make sure there is a  `yesterday.txt` file that: 
    - exists
    - is in the same directory as the `.py` file
    - contains one number between between 1 and 12 and **does not contain anything else**
    - after this set up you will not need to edit or do anything with this file. I inlcude this here so you know you *must* have this file for the script to run. 
    - *(An improvement to this script would be to check whether the file exists and, if not, create it for you)*

-----

## SoundBeat.py
TL script to process Sound Beat (SB) each weekday.
- We are provided 5 episodes of SB per week - one for each weekday. Download them every Monday from Content Depot.
- Place all 5 files in a local folder (delete last week's files)
- Each filename contains `SGMT` followed by a number, such as `SGMT03`.
 - `01` is intended for Monday, `02` for Tuesday, and so on.
 - This script matches the day of the week to a specific filename, then processes that file.

---

## wav.py
Python script to convert audio files of various types to TL broadcast format: mono, 44.1kHz, 16 bit wav files (PCM s16le).
- can be used to convert files from Content Depot
- works fine but needs improvement

---
© Nashville Public Library

© Ben Weddle is to blame for this code. Anyone is free to use it.