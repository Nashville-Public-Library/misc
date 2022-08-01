'''
This is for readying the 105-second Bird Note segment for air.
Please note you must have already downloaded the files and moved them
to the 'BirdNote' folder on the desktop. This should be done each Wednesday.

Once downloaded, there are 7 files - one for each day.
Segment 1 should play Wednesday, 2 Thursday, and so on.
This script ensures the correct file plays on the correct day.

© Nashville Public Library
© Ben Weddle is to blame for this code. Anyone is free to use it.
'''

import subprocess
from datetime import datetime
import shutil
import os
import logging
import logging.handlers
from logging.handlers import SysLogHandler
import smtplib
from email.message import EmailMessage
import time
from twilio.rest import Client
import glob


#-----change these for each new program-----

show = 'Bird Note' # for notifications
output_file = 'Tenn-BirdNote.wav' #name of file with .wav extension
folder = (r'C:\Users\wrprod\Desktop\BirdNote') #path to source files

# these are for checking whether the length (in minutes!) of the file is outside of a range.
# used for notification only
# decimal numbers are OK.
check_if_above = 1.76
check_if_below = 1.74

'''
    -------------------------------------------------------------------------------
        ----------SHOULD NOT NEED TO CHANGE ANYTHING BELOW THIS LINE----------
    -------------------------------------------------------------------------------
'''

# these are defined in the PC's environement variables.
# If you need to change them, change them there, not here!
destinations = [os.environ['OnAirPC'], os.environ['ProductionPC']]

timestamp = datetime.now().strftime('%H:%M:%S on %d %b %Y')

def convert(input):
    '''Convert with ffmpeg and continue'''
    syslog(message=f'{show}: Converting to TL format.')
    # using quotes around input in case the file has spaces in it.
    subprocess.run(f'ffmpeg -hide_banner -loglevel quiet -i "{input}" -ar 44100 -ac 1 -af loudnorm=I=-21 -y {output_file}')
    check_length(fileToCheck=output_file)
    remove(fileToDelete=input)
    copy(fileToCopy=output_file)

def copy(fileToCopy):
    '''
    Copy file to destinations. 
    As for how the number of destinations iteration works, you'll just have to stare at it for a while.
    It took me a while to write and I tried to explain it but cannot.
    '''
    numberOfDestinations = len(destinations)
    numberOfDestinations = numberOfDestinations - 1
    while numberOfDestinations >= 0:
        syslog(message=f'{show}: Copying {fileToCopy} to {destinations[numberOfDestinations]}...')
        shutil.copy(fileToCopy, destinations[numberOfDestinations])
        numberOfDestinations = numberOfDestinations-1
    check_file_transferred(fileToCheck=fileToCopy)

def remove(fileToDelete):
    '''TODO explain'''
    syslog(message=f'{show}: Removing {fileToDelete}')
    os.remove(fileToDelete)

def check_downloaded_file(input_file):
    '''TODO explain'''
    filesize = os.path.getsize(input_file)
    if filesize > 0:
        syslog(message=f'{show}: {input_file} is not empty')
        convert(input=input_file)
    else:
        to_send = (f"There was a problem with {show}.\n\n\
It looks like the file is empty. Please check manually! \
Yesterday's file will remain. \n\n\
{timestamp}")
        notify(message=to_send , subject='Error')        

def syslog(message):
    '''send message to syslog server'''
    host = os.environ["syslog_server"] #IP of PC with syslog server software
    port = int('514')

    my_logger = logging.getLogger('MyLogger')
    my_logger.setLevel(logging.DEBUG)
    handler = SysLogHandler(address = (host, port))
    my_logger.addHandler(handler)

    my_logger.info(message)
    my_logger.removeHandler(handler)

def send_mail(message, subject):
    '''send email to TL gmail account via relay address'''
    mail_server = os.environ["mail_server_external"] #IP of mail server
    format = EmailMessage()
    format.set_content(message)
    format['Subject'] = f'{subject}: {show}'
    format['From'] = "ben.weddle@nashville.gov"
    format['To'] = "nashvilletalkinglibrary@nashville.gov"

    mail = smtplib.SMTP(host=mail_server)
    mail.send_message(format)
    mail.quit()

def send_sms(message):
    '''send sms via twilio. all info is stored in PC's environement variables'''
    twilio_sid = os.environ.get('twilio_sid')
    twilio_token = os.environ.get('twilio_token')
    twilio_from = os.environ.get('twilio_from')
    twilio_to = os.environ.get('twilio_to')

    client = Client(twilio_sid, twilio_token)

    message = client.messages.create(
                        body = message,
                        from_= twilio_from,
                        to = twilio_to
                        )
    message.sid

def notify(message, subject):
    '''TODO: explain'''
    weekend = ['Sat', 'Sun']
    short_day = datetime.now().strftime('%a')
    if short_day in weekend:
        send_sms(message=message) 
        send_mail(message=message, subject=subject)
        syslog(message=message)
    else:
        send_mail(message=message, subject=subject)
        syslog(message=message)

def check_file_transferred(fileToCheck):
    '''check if file transferred to destinations'''
    try:
        numberOfDestinations = len(destinations)
        numberOfDestinations = numberOfDestinations - 1
        while numberOfDestinations >= 0:
            os.path.isfile(f'{destinations[numberOfDestinations]}\{fileToCheck}')
            numberOfDestinations = numberOfDestinations-1
            syslog(message=f'{show} arrived at {destinations[numberOfDestinations]}')
        remove(fileToDelete=output_file)
        countdown()
    except:
        to_send = (f"There was a problem with {show}.\n\n\
It looks like the file either wasn't converted or didn't transfer correctly. \
Please check manually! \n\n\
{timestamp}")
        notify(message=to_send, subject='Error')
        os.system('cls')
        print(to_send)  # get user's attention!
        print()
        # force user to acknowledge by closing window
        input('(press enter to close this window)')

def check_length(fileToCheck):
    '''check length of converted file with ffprobe. if too long or short, send notification'''
    duration = subprocess.getoutput(f"ffprobe -v error -show_entries format=duration \
    -of default=noprint_wrappers=1:nokey=1 {fileToCheck}")
    duration = float(duration)
    duration = round(duration)
    duration = duration/60
    
    if duration > check_if_above:
        to_send = (f"Today's {show} is {duration} minutes long! \
Please check manually and make edits to bring it below {check_if_above} minutes.\n\n\
{timestamp}")
        notify(message=to_send, subject='Check Length')
    elif duration < check_if_below:
        to_send = (f"Today's {show} is only {duration} minutes long! \
This is unusual and could indicate a problem with the file. Please check manually!\n\n\
{timestamp}")
        notify(message=to_send, subject='Check Length')
    else: syslog(message=f'{show} is {duration} minute(s)')

#TODO: explain what this is doing!
def match_name():
    global source_exists
    source_exists = False
    dict = {
    'Wed': 'SGMT01',
    'Thu': 'SGMT02',
    'Fri': 'SGMT03',
    'Sat': 'SGMT04',
    'Sun': 'SGMT05',
    'Mon': 'SGMT06',
    'Tue': 'SGMT07'
    }
    day_abbr = datetime.now().strftime("%a")
    sgmt = dict.get(day_abbr)
    sourceFileExists = False
    fileToUse = None
    for file in glob.glob(f'{folder}\*.wav'):
        if sgmt in file:
            syslog(message=f'{show}: Attempting to use segment: {sgmt}')
            fileToUse = file
            sourceFileExists = True
    return sourceFileExists, fileToUse

def countdown():
    '''
        the reason for this is to give a visual cue to the user
        that the script has finished and is about to exit.
        Otherwise, the user does not know what happened; they
        just see the screen disappear.
    '''
    os.system('cls')
    toSend = f'{show}: All Done.'
    syslog(message=toSend)
    print(toSend)
    print()
    number = 5
    i = 0
    while i < number:
        print(f'This window will close in {number} seconds...', end='\r')
        number = number-1
        time.sleep(1)

#BEGIN
if __name__ == "__main__":
    print(f"I'm working on {show}. Just a moment...")
    syslog(message=f'{show}: Starting script')

    fileExists, pathToFile = match_name()
    if fileExists == True:
        check_downloaded_file(input_file=pathToFile)
    else:
        to_send = (f"There was a problem with {show}. \n\n\
It looks like the source file doesn't exist. \
Please check manually! Yesterday's file will remain.\n\n\
{timestamp}")
        notify(message=to_send, subject='Error')
        os.system('cls')
        print(to_send)
        print()
        input('(press enter to close this window)') #force user to acknowledge