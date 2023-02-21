'''
Send metadata to Icecast and wherever else you need it.
I haven't yet figured out how to get this to work with Python's socket library,
so we're using ncat.
Just call up this script from the command line or a bash/batch script and pass
in the command line argument.
'''
import argparse
import socket

from talklib.show import TLShow

parser = argparse.ArgumentParser()
parser.add_argument('--title', type=str, required=True)
args = parser.parse_args()
title = args.title

send_syslog = TLShow(show=f'Metadata')

error_message = f'There was a problem sending metadata for "{title}".'

# Telos
try:
    host = '10.28.30.129'
    port = 9000

    to_send = f'<song title="{title}" url="..."></song>'
    to_send = to_send.encode()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    sock.sendall(to_send)
    sock.close()
    send_syslog.syslog(message=f'{title} sent to Telos')
except:
    send_syslog.syslog(message=error_message)


# BrightSign 
try:
    to_send_UDP = title.encode()
    serverAddressPort   = ("10.28.30.212", 5000)
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPClientSocket.sendto(to_send_UDP, serverAddressPort)
    send_syslog.syslog(message=f'{title} sent to BrightSign')
except:
    send_syslog.syslog(message=error_message)