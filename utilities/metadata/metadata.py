'''
Send metadata to Icecast and wherever else you need it.
TCP is for Telos, UDP is for BrightSign.

Just call up this script from the command line or a batch script and pass
in the command line argument.
'''

import argparse
import socket

from talklib.notify import Notify
from talklib.utils import metadata_to_icecast


def get_title():
    parser = argparse.ArgumentParser()
    parser.add_argument('--title', type=str, required=True)
    args = parser.parse_args()
    title = args.title
    return title

def send_to_BrightSign(title):
    try:
        notify = Notify()
        notify.syslog.send_syslog_message(message=f'attempting to send "{title}" to BrightSign')
        to_send_UDP = title.encode()
        serverAddressPort   = ("10.28.30.212", 5000)
        UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        UDPClientSocket.sendto(to_send_UDP, serverAddressPort)
        notify.syslog.send_syslog_message(message=f'Successfully sent {title}" to BrightSign')
    except:
        to_send = f'There was a problem sending {title} to the BrightSign unit'
        notify.syslog.send_syslog_message(message=to_send, level='error')
        notify.send_mail(subject='Error', message=to_send)


def main():
    title = get_title()
    print(f'...sending "{title}..."')
    metadata_to_icecast(title=title)
    send_to_BrightSign(title=title)

main()