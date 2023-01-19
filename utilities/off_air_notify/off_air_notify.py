'''
This script is called from the batch script which is called directly from the syslog server when it receives an SNMP trap message
from the silence sensor. It sends an outbound voice call and sms message with the message below.
To change things, adjust the settings in the syslog server.
'''

import argparse
from datetime import datetime
import os
from talklib.show import TLShow

from twilio.rest import Client

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

# TLShow().syslog(message=arg1)
# TLShow().syslog(message=feed_name)


# body of the phone call and sms
message = f"There is a problem with the Talking Library broadcast. The {feed_name} feed is down. \
There is more information in the email I just sent you. Please take a look and address the issue. Thank you."

twilio_sid = os.environ.get('twilio_sid')
twilio_token = os.environ.get('twilio_token')
twilio_from = os.environ.get('twilio_from')
twilio_to = os.environ.get('twilio_to')

def time_of_day():
    '''
    to determine whether to say good morning, afternoon, or evening. 
    This is not really necessary, to be honest...'''
    morning = ['04', '05', '06', '07', '08', '09', '10', '11']
    evening = ['18', '19', '20', '21', '22', '23', '00', '01', '02', '03']
    afternoon = ['12', '13', '14', '15', '16', '17']
    current_time = datetime.now().strftime('%H')
    if current_time in morning:
        which_phrase = "Good morning."
    elif current_time in evening:
        which_phrase = "Good evening."
    elif current_time in afternoon:
        which_phrase = "Good Afternoon."
    else: which_phrase = 'Hello.'
    
    return(which_phrase)

def send_call(greeting):
    '''send voice call via twilio'''
    client = Client(twilio_sid, twilio_token)

    call = client.calls.create(
                            twiml=f'<Response><Say>{greeting} {message}</Say></Response>',
                            to=twilio_to,
                            from_=twilio_from
                        )
    call.sid

def send_sms():
    '''send sms via twilio'''
    client = Client(twilio_sid, twilio_token)

    sms = client.messages.create(
                        body = message,
                        from_= twilio_from,
                        to = twilio_to
                        )
    sms.sid

greeting = time_of_day()
send_sms()
send_call(greeting)
