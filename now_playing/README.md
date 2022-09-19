# nowplaying

Several different methods to parse the public-facing part of the TL Icecast server and return the Now Playing metadata (Icecast calls this "Current Song").

-----

**JS/HTML**

The JS file outputs the text to the browser console. This script is included in the console_log.HTML file.

The TLNowPlaying.HTML file is an example of including the script directly on a page, and outputting to an HTML tag.

**PHP**

ReturnAll.php returns all fields from Icecast, which is useful for testing.

ReturnOne.php returns only "Current Song".

**Python**

NowPlaying-ET.py uses ElementTree, but credentials are required to access the raw xml.

NowPlaying-LXML.py uses lxml (and xpath). No credentials are needed.

---
© Nashville Public Library

© Ben Weddle is to blame for this code. Anyone is free to use it.
