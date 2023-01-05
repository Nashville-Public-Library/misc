import subprocess
import argparse

from talklib.show import TLShow

parser = argparse.ArgumentParser()
parser.add_argument('--title', type=str, required=True)
args = parser.parse_args()
title = args.title

a = TLShow(show=f'Metadata')
to_send = f'There was a problem sending metadata for {title}'

try:
    subprocess.run(f'echo t={title} | ncat %Telos%', shell=True, timeout=5)
    a.syslog(message=f' {title} sent to encoder')
except:
    a.notify(message=to_send, subject='Error')

try:
    subprocess.run(f'echo {title} | ncat -u %BrightSign%', shell=True, timeout=5)
    a.syslog(message=f' {title} sent to BrightSign')
except Exception as b:
    a.notify(message=to_send, subject='Error')