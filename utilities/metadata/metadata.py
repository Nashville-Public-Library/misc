import subprocess
import argparse

from talklib.show import TLShow

parser = argparse.ArgumentParser()
parser.add_argument('--title', type=str, required=True)
args = parser.parse_args()
title = args.title

object_for_notifications = TLShow(show=f'Metadata')

error_message = f'There was a problem sending metadata for {title}'
success_message = f' "{title}" sent to encoder'

# send message to Telos unit
try:
    subprocess.run(f'echo t={title} | ncat 10.28.30.129 9000', shell=True, timeout=5)
    object_for_notifications.syslog(message=success_message)
except:
    object_for_notifications.notify(message=error_message, subject='Error')

# send message to BrightSign unit
try:
    subprocess.run(f'echo {title} | ncat -u 10.28.30.212 5000', shell=True, timeout=5)
    object_for_notifications.syslog(message=success_message)
except:
    object_for_notifications.notify(message=error_message, subject='Error')