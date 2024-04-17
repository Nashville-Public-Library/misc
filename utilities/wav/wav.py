'''
Converts audio files to TL format

© Nashville Public Library
© Ben Weddle is to blame for this code. Anyone is free to use it.
'''

import glob
import os
import subprocess

supported_formats = ['mp3', 'wav', 'm4a', 'flac']
cd = os.getcwd() #current directory
yes = ['yes', 'y']

def scan_files():
    file_types = glob.glob(f'*.{supported_formats[0]}') + glob.glob(f'*.{supported_formats[1]}') + \
        glob.glob(f'*.{supported_formats[2]}') + glob.glob(f'*.{supported_formats[3]}')
    return file_types

def convert(file):
    '''convert file with ffmpeg, etc. TODO, add better explanation'''
    subprocess.run('cls', shell=True)
    print(f'Converting {file}...')
    subprocess.run(f'ffmpeg -hide_banner -loglevel quiet -i "{file}" -ac 1 -ar 44100 output.wav', shell=True)
    os.remove(file)
    os.rename("output.wav", file)
    base = os.path.splitext(file)[0]
    os.rename(file, base + '.wav')
    subprocess.run('cls', shell=True)

def check_exists():
    '''check whether there are any audio files in current directory'''
    if len(scan_files()) >= 1:
        return scan_files
    else:
        False

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
    if not check_exists():
        subprocess.run('cls', shell=True)
        print(f"--------------------CONVERT--------------------\n\n\
I can't find any {supported_formats} files in {cd}. Sorry about that.\n\n\
Do you want to try again?\n")
        answer = input('Y/N ')
        if answer in yes:
            prompt()
        else:
            quit()

    print('The following file(s) will be converted: \n')
    for file in scan_files():
        print(file)
    print('\nAre you sure you want to convert these files? It cannot be undone.\n')

    answer = input('Y/N ')
    if answer.lower() in yes:
        for f in scan_files():
            convert(file=f)
        print('Your files are converted. Enjoy\n')
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
