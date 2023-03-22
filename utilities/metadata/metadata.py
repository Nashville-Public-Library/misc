'''
Send metadata to Icecast and wherever else you need it.
Currently, this is sending to the TL Telos encoder unit,
AND to the BrightSign unit.
TCP is for Telos, UDP is for BrightSign.

Just call up this script from the command line or a batch script and pass
in the command line argument.
'''

import argparse
import os
import socket

import requests

from talklib.show import TLShow

meta = TLShow(show=f'Metadata')

def get_title():
    parser = argparse.ArgumentParser()
    parser.add_argument('--title', type=str, required=True)
    args = parser.parse_args()
    title = args.title
    return title

def send_to_icecast(title):
    meta.syslog(message=f'attempting to send "{title}" to Icecast')
    user = os.environ['icecast_user']
    password = os.environ['icecast_pass']
    url = f'https://npl.streamguys1.com:80/admin/metadata?mount=/live&mode=updinfo&song={title}'
    send = requests.get(url, auth = (user, password))
    if send.status_code != 200:
        meta.notify(
            subject='Error', 
            message=f'There was a problem sending metadata to Icecast. The response code was: {send.status_code}'
            )
    else:
        meta.syslog(message=f'"{title}" sent to Icecast')


def send_to_BrightSign(title):
    try:
        meta.syslog(message=f'attempting to send "{title}" to BrightSign"')
        to_send_UDP = title.encode()
        serverAddressPort   = ("10.28.30.212", 5000)
        UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        UDPClientSocket.sendto(to_send_UDP, serverAddressPort)
        meta.syslog(message=f'"{title}" sent to BrightSign')
    except:
        meta.notify(subject='Error', message=f'There was a problem sending the title to the BrightSign unit')


def main():
    title = get_title()
    print(f'...sending "{title}..."')
    send_to_icecast(title=title)
    send_to_BrightSign(title=title)

main()