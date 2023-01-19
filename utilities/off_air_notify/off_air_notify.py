'''
This script is called from the batch script which is called directly from the syslog server when it receives an SNMP trap message
from the silence sensor. It sends an outbound voice call and sms message with the message below.
To change things, adjust the settings in the syslog server.
'''

import argparse

from talklib.utils import send_sms, send_call

parser = argparse.ArgumentParser()
parser.add_argument('--feed_name', type=str, required=True)
args = parser.parse_args()
arg1 = args.feed_name

if 'wpln' in arg1:
    feed_name = 'WPLN stream'
elif 'SCA' in arg1:
    feed_name = 'radio'
elif 'live' in arg1:
    feed_name = 'public stream'
else:
    feed_name = 'unknown'


# body of the phone call and sms
message = f"There is a problem with the Talking Library broadcast. The {feed_name} feed is down. \
There is more information in the email I just sent you. Please take a look and address the issue. Thank you."

send_sms(message=message)
send_call(message=message)

