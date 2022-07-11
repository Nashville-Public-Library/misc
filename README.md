# MISC 

MISC Python scripts to automate various tasks at the TL.

For *all* these scripts, **you must have a Windows [FFmpeg](https://www.ffmpeg.org) binary installed and added to the PATH**. FFmpeg is open source (and free!) software.

Some scripts also use Twilio, which is not in the Python standard library and needs to be installed via PIP. Store the Twilio credentials in environment variables on the PCs.

Actually, a number of variables used in these scripts are stored in environment variables. Make sure to check those.

We run most of these scripts via WireReady (WR).
- The "Run" command in WR defaults to running from a different directory AND a different drive letter. This causes confusion.
- WR also does not run `.py` files by default. For this reason and more, we do not run `.py` files directly from WR.
- Instead, we tell WR to run a Batch script (`.bat` file) which in turn will run the Python script (`.py` file). 
- The batch script ensures we CD to the current directory.
- Ensure the Batch & Python scripts are in the same directory.
- A sample `.bat` file (`Example.bat`) is inlcuded in this repo.

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
    - contains a single number between between 1 and 12 and does not contain anything else
    - after this set up you will not need to edit or do anything with this file. I inlcude this here so you know you *must* have this file for the script to run. TODO An improvement to this script would be to check whether the file exists and, if not, create it for you.

---

## wav.py
Python script to convert audio files of various types to TL broadcast format (mono, 44.1kHz, 16 bit wav files).
- can be used to convert files from Content Depot
- works fine but needs improvement