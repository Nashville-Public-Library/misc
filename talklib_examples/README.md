# talklib_examples 
## Using the talklib module

Animal Airwaves, Bird Note, and Sound Beat are all shows whose files we download ahead of time. They all use the [talklib](https://github.com/talkinglibrary/talklib) library. The way we go about selecting which file to process is unique to each show, so here is some information about how it works and why we're doing it this way.

----

## AnimalAir.py

TL script to process Animal Airwaves (AA) each day.
- We are provided 12 episodes of AA per month. Download them all together at the beginning of each month from Content Depot.
- Place all 12 files in the local folder listed in the script (delete last month's files).
- Since there are only 12 episodes, but we need to air it every day, we will usually need to air each episode more than once.
- The script will randomize which episode is used each day and also ensure the same episode never airs two days in a row.
- Make sure there is a  `yesterday.txt` file that: 
    - exists
    - is in the same directory as the `.py` file
    - contains one number between between 1 and 12 and **does not contain anything else**
    - after this set up you will not need to edit or do anything with this file. I inlcude this here so you know you *must* have this file for the script to run. 
    - *(An improvement to this script would be to check whether the file exists and, if not, create it for you)*
- Note that the original source files are *not* deleted when the script runs. This is because we re-air them throughout the month.

----
## BirdNote.py

TL script to process Bird Note (BN) each weekday.
- We are provided 7 episodes of BN per week - one for each day of the week. Download them all together every Wednesday from Content Depot.
- Place all 7 files in the local folder listed in the script. There should not be any files remaining in the folder on Wednesday, but if there are, delete them.
- Each filename contains `SGMT` followed by a number, such as `SGMT05`.
 - `01` is intended for Wednesday, `02` for Thursday, ... and `07` is for Tuesday.
 - This script matches the day of the week to a specific filename, then processes that file.

----
## HealthHeart.py

TL script to process Health in a Heartbeat (HH) each weekday.
- We are provided one episode for each weekday of the month. Download them all together on the first weekday of the month from Content Depot.
- Place all files in the local folder listed in the script. There should not be any files remaining in the HH folder at the beginning of the month, but if there are, delete them first.
- Each filename contains `SGMT` followed by a number, such as `SGMT03`.
    - IMPORTANT: The first file, labelled with `SGMT01`, is an empty audio file. Delete it!
    - The first file should be `SGMT02`.
- This script will look at all the files in this folder and pick the file with the lowest SGMT number to use.
----
## SoundBeat.py

TL script to process Sound Beat (SB) each weekday.
- We are provided 5 episodes of SB per week - one for each weekday. Download them all together every Monday from Content Depot.
- Place all 5 files in the local folder listed in the script. There should not be any files remaining in the SB folder on Monday, but if there are, delete them.
- Each filename contains `SGMT` followed by a number, such as `SGMT03`.
 - `01` is intended for Monday, `02` for Tuesday, and so on.
 - This script matches the day of the week to a specific filename, then processes that file.

----
© Nashville Public Library

© Ben Weddle is to blame for this code. Anyone is free to use it.