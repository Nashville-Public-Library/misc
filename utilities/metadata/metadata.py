'''
Send metadata to Icecast and wherever else you need it.
I haven't yet figured out how to get this to work with Python's socket library,
so we're using ncat.

Just call up this script from the command line or a bash/batch script and pass
in the command line argument.
'''

import subprocess
import argparse
import time

from talklib.show import TLShow

parser = argparse.ArgumentParser()
parser.add_argument('--title', type=str, required=True)
args = parser.parse_args()
title = args.title

send_syslog = TLShow(show=f'Metadata')

error_message = f'There was a problem sending metadata for "{title}".'
success_message = f' "{title}" sent to encoder'

# send message to Telos unit
try:
    send = subprocess.Popen(f'echo t={title} | ncat 10.28.30.129 9000', shell=True)
    send_syslog.syslog(message=success_message)
    time.sleep(4)
    send.kill()
except Exception as asdf:
    error_message = error_message + 'Here is the error: ' + asdf
    send_syslog.notify(message=error_message, subject='Error')


try:
    send = subprocess.Popen(f'echo {title} | ncat -u 10.28.30.212 5000', shell=True,)
    send_syslog.syslog(message=success_message)
    time.sleep(4)
    send.kill()
except Exception as asdf:
    error_message = error_message + 'Here is the error: ' + asdf
    send_syslog.notify(message=error_message, subject='Error')