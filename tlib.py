'''
TL library for processing RSS shows and other segments.
It's best to read the docs.

© Nashville Public Library
© Ben Weddle is to blame for this code. Anyone is free to use it.
'''

from xml.etree.ElementInclude import include
import xml.etree.ElementTree as ET
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
import requests
import glob

# these are defined in the PC's environement variables.
# If you need to change them, change them there, not here!
destinations = [os.environ['OnAirPC'], os.environ['ProductionPC']]
fromEmail = os.environ['fromEmail']  # from where should emails appear to come?
toEmail = os.environ['toEmail']  # to where should emails be sent?

short_day = datetime.now().strftime('%a')
timestamp = datetime.now().strftime('%H:%M:%S on %d %b %Y')


class tlshow:
    '''write something here'''
    def __init__(self, show=None, showFilename=None, url=None, include_date=False, is_local=False, local_file=None, remove_source=False, check_if_above=0, check_if_below=0, notifications=True):
        self.show = show
        self.showFilename = showFilename
        self.url = url
        self.include_date = include_date
        self.is_local = is_local
        self.local_file = local_file
        self.remove_source = remove_source
        self.check_if_above = check_if_above    
        self.check_if_below = check_if_below
        self.notifications = notifications

    def convert(self, input):
        '''convert file with ffmpeg and proceed'''
        if self.include_date:
            date = datetime.now().strftime("%m%d%y")
            outputFile = (f"{self.showFilename}-{date}.wav")
        else: 
            outputFile = (f'{self.showFilename}.wav')

        tlshow.syslog(self, message=f'{self.show}: Converting to TL format.')
        subprocess.run(f'ffmpeg -hide_banner -loglevel quiet -i {input} -ar 44100 -ac 1 -af loudnorm=I=-21 -y {outputFile}')
        if self.check_if_below > 0:
            tlshow.check_length(self, fileToCheck=outputFile) # call this before removing the files
        if self.url:
            tlshow.remove(self, fileToDelete=input)
        elif self.local_file:
            if self.remove_source == True:
                tlshow.remove(self, fileToDelete=input)
        tlshow.copy(self, fileToCopy=outputFile)


    def copy(self, fileToCopy):
        '''TODO explain'''
        numberOfDestinations = len(destinations)
        numberOfDestinations = numberOfDestinations - 1
        while numberOfDestinations >= 0:
            tlshow.syslog(self, message=f'{self.show}: Copying {fileToCopy} to {destinations[numberOfDestinations]}...')
            shutil.copy(fileToCopy, destinations[numberOfDestinations])
            numberOfDestinations = numberOfDestinations-1
        tlshow.remove(self, fileToDelete=fileToCopy)
        tlshow.check_file_transferred(self, fileToCheck=fileToCopy)


    def remove(self, fileToDelete):
        '''TODO explain'''
        tlshow.syslog(self, message=f'{self.show}: Deleting {fileToDelete}')
        os.remove(fileToDelete)  # remove original file from current directory


    def removeYesterdayFiles(self):
        '''delete yesterday's files from destinations. 
        OK to use glob wildcards since there should only ever be one file'''

        numberOfDestinations = len(destinations)
        numberOfDestinations = numberOfDestinations - 1

        while numberOfDestinations >= 0:
            globbify = glob.glob(
                f'{destinations[numberOfDestinations]}\{self.showFilename}*.wav')
            globbifyLength = len(globbify) - 1
            if globbifyLength >= 0:
                tlshow.syslog(self, message=f'{self.show}: Deleting {globbify[globbifyLength]}')
                os.remove(f'{globbify[globbifyLength]}')
            else:
                tlshow.syslog(self, message=f"{self.show}: Cannot find yesterday's files. Continuing...")
            numberOfDestinations = numberOfDestinations - 1
            globbifyLength = globbifyLength - 1


    def download_file(self):
        '''download audio file from rss feed'''
        download = tlshow.get_audio_url(self)
        tlshow.syslog(self, message=f'{self.show}: Attempting to download audio file.')
        input_file = 'input.mp3'  # name the file we download
        # using wget because urlretrive is getting a 403 denied error
        subprocess.run(f'wget -q -O {input_file} {download}')
        tlshow.check_downloaded_file(self, fileToCheck=input_file)


    def check_downloaded_file(self, fileToCheck):
        '''TODO explain'''
        filesize = os.path.getsize(fileToCheck)
        is_not_empty = False
        i = 0
        while i < 3:
            if filesize > 0:
                tlshow.syslog(self, message=f'{self.show} is not empty. Continuing...')
                tlshow.convert(self, input=fileToCheck)
                is_not_empty = True
                break
            else:
                tlshow.syslog(self, message=f'{self.show} is empty. Will download again. Attempt # {i}.')
                tlshow.download_file(self)
                i = i+1
        if is_not_empty == True:
            pass
        else:
            toSend = (f"There was a problem with {self.show}.\n\n\
    It looks like the downloaded file is empty. Please check manually! \
    Yesterday's file will remain. \n\n\
    {timestamp}")
            tlshow.notify(self, message=toSend, subject='Error')


    def syslog(self, message):
        '''send message to syslog server'''
        host = os.environ["syslog_server"]  # IP of PC with syslog server software
        port = int('514')

        my_logger = logging.getLogger('MyLogger')
        my_logger.setLevel(logging.DEBUG)
        handler = SysLogHandler(address=(host, port))
        my_logger.addHandler(handler)

        my_logger.info(message)
        my_logger.removeHandler(handler) # don't forget this after you send the message!


    def send_mail(self, message, subject):
        '''send email to TL gmail account via relay address'''
        mail_server = os.environ["mail_server_external"]  # IP of mail server
        format = EmailMessage()
        format.set_content(message)
        format['Subject'] = f'{subject}: {self.show}'
        format['From'] = fromEmail
        format['To'] = toEmail

        mail = smtplib.SMTP(host=mail_server)
        mail.send_message(format)
        mail.quit()


    def send_sms(self, message):
        '''send sms via twilio. all info is stored in PC's environement variables'''
        twilio_sid = os.environ.get('twilio_sid')
        twilio_token = os.environ.get('twilio_token')
        twilio_from = os.environ.get('twilio_from')
        twilio_to = os.environ.get('twilio_to')

        client = Client(twilio_sid, twilio_token)

        message = client.messages.create(
            body=message,
            from_=twilio_from,
            to=twilio_to
        )
        message.sid


    def notify(self, message, subject):
        '''TODO: explain'''
        if self.notifications:
            weekend = ['Sat', 'Sun']
            if short_day in weekend:
                tlshow.send_sms(self, message=message)
                tlshow.send_mail(self, message=message, subject=subject)
                tlshow.syslog(self, message=message)
            else:
                tlshow.send_mail(self, message=message, subject=subject)
                tlshow.syslog(self, message=message)
        else:
            pass


    def check_file_transferred(self, fileToCheck):
        '''check if file transferred to OnAir PC'''
        try:
            numberOfDestinations = len(destinations)
            numberOfDestinations = numberOfDestinations - 1
            while numberOfDestinations >= 0:
                os.path.isfile(
                    f'{destinations[numberOfDestinations]}\{fileToCheck}')
                numberOfDestinations = numberOfDestinations-1
                tlshow.syslog(self, message=f'{self.show}: {fileToCheck} arrived at {destinations[numberOfDestinations]}')
            tlshow.countdown(self)
        except:
            toSend = (f"There was a problem with {self.show}.\n\n\
    It looks like the file either wasn't converted or didn't transfer correctly. \
    Please check manually! \n\n\
        {timestamp}")
            tlshow.notify(self, message=toSend, subject='Error')
            os.system('cls')
            print(toSend)  # get user's attention!
            print()
            input('(press enter to close this window)') # force user to acknowledge by closing window


    def check_length(self, fileToCheck):
        '''check length of converted file with ffprobe. if too long or short, send notification'''
        duration = subprocess.getoutput(f"ffprobe -v error -show_entries format=duration \
        -of default=noprint_wrappers=1:nokey=1 {fileToCheck}")
        duration = float(duration)
        duration = duration/60
        duration = round(duration, 2)

        if duration > self.check_if_above:
            toSend = (f"Today's {self.show} is {duration} minutes long! \
    Please check manually and make edits to bring it below {self.check_if_above} minutes.\n\n\
    {timestamp}")
            tlshow.notify(self, message=toSend, subject='Check Length')
        elif duration < self.check_if_below:
            toSend = (f"Today's {self.show} is only {duration} minutes long! \
    This is unusual and could indicate a problem with the file. Please check manually!\n\n\
    {timestamp}")
            tlshow.notify(self, message=toSend, subject='Check Length')
        else:
            tlshow.syslog(self, message=f'{self.show}: File is {duration} minute(s). Continuing...')


    def get_feed(self):
        '''check if today's file has been uploaded'''
        header = {'User-Agent': 'Darth Vader'}  # usually helpful to identify yourself
        rssfeed = requests.get(self.url, headers=header)
        rssfeed = rssfeed.text
        rssfeed = ET.fromstring(rssfeed)
        return rssfeed


    def check_feed_updated(self):
        '''TODO explain'''
        root = tlshow.get_feed(self)
        for t in root.findall('channel'):
            item = t.find('item')  # 'find' only returns the first match!
            pub_date = item.find('pubDate').text
            if short_day in pub_date:
                tlshow.syslog(self, message=f'{self.show}: The feed is updated. Continuing...')
                return True


    def get_audio_url(self):
        '''TODO: explain'''
        root = tlshow.get_feed(self)
        for t in root.findall('channel'):
            item = t.find('item')  # 'find' only returns the first match!
            audio_url = item.find('enclosure').attrib
            audio_url = audio_url.get('url')
            tlshow.syslog(self, message=f'{self.show}: Audio URL is: {audio_url}')
            return audio_url


    def check_feed_loop(self):
        '''for some reason the first time we check the feed, it is not showing as updated.
        It's being cached, or something...? So we are checking it 3 times, for good measure.'''
        i = 0
        while i < 3:
            tlshow.syslog(self, message=f'{self.show}: Attempt {i} to check feed.')
            feed_updated = tlshow.check_feed_updated(self)
            if feed_updated == True:
                return feed_updated
            else:
                time.sleep(1)
                i = i+1


    def countdown(self):
        os.system('cls')
        toSend = f'{self.show}: All Done.'
        tlshow.syslog(self, message=toSend)
        print(toSend)
        print()
        number = 5
        i = 0
        while i < number:
            print(f'This window will close in {number} seconds...', end='\r')
            number = number-1
            time.sleep(1)


    def lets_run(self):
        '''Begins to process the file'''
        
        print((f"I'm working on {self.show}. Just a moment..."))
        tlshow.syslog(self, message=f'{self.show}: Starting script')

        if not self.show:
            raise Exception ('Sorry, you need to specify a show name.')

        if not self.showFilename:
            raise Exception ('Sorry, you need to specify a show abbreviation name.')

        if self.url and self.is_local:
            raise Exception ('Sorry, you cannot specify both a URL and a local audio file. You must choose only one.')

        if self.check_if_above == 0 or self.check_if_below == 0:
            print()
            print('(You did not specify check_if_below and/or check_if_above. These tests will not be run.')
        
        if self.url:
            if tlshow.check_feed_loop(self) == True:
                tlshow.removeYesterdayFiles(self)
                tlshow.download_file(self)
            else:
                toSend = (f"There was a problem with {self.show}. \n\n\
    It looks like today's file hasn't yet been posted. \
    Please check and download manually! Yesterday's file will remain.\n\n\
    {timestamp}")
                tlshow.notify(self, message=toSend, subject='Error')
                os.system('cls')
                print(toSend)
                print()
                input('(press enter to close this window)')  # force user to acknowledge
        elif self.is_local:
            if self.local_file:
                tlshow.check_downloaded_file(self, fileToCheck=self.local_file)
            else:
                to_send = (f"There was a problem with {self.show}. \n\n\
    It looks like the source file doesn't exist. \
    Please check manually! Yesterday's file will remain.\n\n\
    {timestamp}")
                tlshow.notify(self, message=to_send, subject='Error')
                os.system('cls')
                print(to_send)
                print()
                input('(press enter to close this window)') #force user to acknowledge      
        else:
            raise Exception ('Sorry, you need to specify either a URL or local audio file. \
Did you set is_local to True?')
        

#         if self.url:
#             if tlshow.check_feed_loop(self) == True:
#                 tlshow.removeYesterdayFiles(self)
#                 tlshow.download_file(self)
#             else:
#                 toSend = (f"There was a problem with {self.show}. \n\n\
#     It looks like today's file hasn't yet been posted. \
#     Please check and download manually! Yesterday's file will remain.\n\n\
#     {timestamp}")
#                 tlshow.notify(self, message=toSend, subject='Error')
#                 os.system('cls')
#                 print(toSend)
#                 print()
#                 input('(press enter to close this window)')  # force user to acknowledge
        
#         if self.is_local and self.local_file != None:
#             tlshow.check_downloaded_file(self, fileToCheck=self.local_file)
#         else:
#             to_send = (f"There was a problem with {self.show}. \n\n\
# It looks like the source file doesn't exist. \
# Please check manually! Yesterday's file will remain.\n\n\
# {timestamp}")
#             tlshow.notify(self, message=to_send, subject='Error')
#             os.system('cls')
#             print(to_send)
#             print()
#             input('(press enter to close this window)') #force user to acknowledge
