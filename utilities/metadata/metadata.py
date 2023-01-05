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

try:
    subprocess.run(f'echo t={title} | ncat %Telos%', shell=True, timeout=5)
    object_for_notifications.syslog(message=success_message)
except:
    object_for_notifications.notify(message=error_message, subject='Error')

try:
    subprocess.run(f'echo {title} | ncat -u %BrightSign%', shell=True, timeout=5)
    object_for_notifications.syslog(message=success_message)
except:
    object_for_notifications.notify(message=error_message, subject='Error')