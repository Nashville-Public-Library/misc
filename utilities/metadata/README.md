# utilities
## metadata.py

TL script to send "Now Playing" metadata to Icecast and elsewhere.

### How to use this script

Place this Python script somehwere in your WireReady directory (E.G. `D:\wireready\Meta\`)

To send metadata to Icecast, use the template in the batch file from this repository (metadata.bat) and just change the name of the program. 

Create a new batch file for every new program title you need to send to Icecast. 

Schedule the batch file to run at the appropriate time via WireReady.

### Dependencies
 - The TL's [talklib](https://github.com/talkinglibrary/talklib) module must be installed.
    - Instructions for downloading/installation are on the GitHub page.

---
© Nashville Public Library

© Ben Weddle is to blame for this code. Anyone is free to use it.