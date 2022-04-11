'''
Converts audio files to TL format

© Nashville Public Library
© Ben Weddle is to blame for this code. Anyone is free to use it.
'''

import glob
import os
import subprocess

supported_formats = ['mp3', 'wav', 'm4a', 'flac']

file_types = glob.glob(f'*.{supported_formats[0]}') + glob.glob(f'*.{supported_formats[1]}') + \
glob.glob(f'*.{supported_formats[2]}') + glob.glob(f'*.{supported_formats[3]}')

cd = os.getcwd() #current directory

yes = ['yes', 'Yes', 'YES' 'Y', 'y']

def convert(file):
    '''convert file with ffmpeg, etc. TODO, add better explanation'''
    subprocess.run('cls', shell=True)
    print('Just a moment...')
    subprocess.run(f'ffmpeg -hide_banner -loglevel quiet -i "{file}" -ac 1 -ar 44100 output.wav', shell=True)
    #when converting to exe file, change the above line to:
    #os.system(resource_path("ffmpeg -hide_banner -loglevel quiet -i input.mp3 -ar 44100 -ac 1 output.wav"))
    os.remove(file)
    os.rename("output.wav", file)
    base = os.path.splitext(file)[0]
    os.rename(file, base + '.wav')
    subprocess.run('cls', shell=True)

def check_exists():
    '''check whether there are any audio files in current directory'''
    if len(file_types) >= 1:
        pass
    else:
        subprocess.run('cls', shell=True)
        print(f"I can't find any {supported_formats} files in {cd}. Sorry about that.\n\n\
Do you want to try again?\n")
        answer = input('Y/N ')
        if answer in yes:
            prompt()
        else:
            quit()
def quit():
    '''print message and exit script'''
    subprocess.run('cls', shell=True)
    print('Thanks, have a good one.')
    print()
    input('(press enter to quit)')
    exit()

def prompt():
    '''print welcome message, ask if user is sure they want to proceed. depending on answer, call functions.'''
    subprocess.run('cls', shell=True)
    print('--------------------CONVERT--------------------')
    print()
    print(f'This will convert the audio files in {cd} to WAV files')
    print()
    print('Are you sure you want to convert these files? It cannot be undone.')
    print()
    answer = input('Y/N ')
    if answer in yes:
        check_exists()
        for f in file_types:
            convert(file=f)
        print('Your files are converted. Enjoy')
        print()
        input('(press enter to quit)')
    else:
        subprocess.run('cls', shell=True)
        not_yes = input(f'You typed {answer}, so nothing was converted. \n\n\
type "y" to start over or anything else to quit: ')
        if not_yes in yes:
            prompt()
        else:
            quit()

prompt()
