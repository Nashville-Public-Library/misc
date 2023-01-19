# utilities
## off_air_notify.py

TL script to notify staff of an off-air incident via SMS and phone call, which are sent via Twilio.

The TL's silence sensor monitors several feeds for silence. When detected, the sensor sends SNMP messages to our Syslog server. When the Syslog server receives a message matching certain keywords, it will exexcute the Batch script with a command line argument (the name of the feed that has gone silent). The Batch script then executes the Python script - with the command line argument - which then connects to Twilio and sends the message out.

### Dependencies
 - The TL's 'talklib' module must be installed!

---
© Nashville Public Library

© Ben Weddle is to blame for this code. Anyone is free to use it.