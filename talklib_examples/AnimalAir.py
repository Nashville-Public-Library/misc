from talklib.show import TLShow
import random
import glob


def guessNumber():
    guess = random.randint(1, 12)
    guess = (f'{guess:02d}')
    guess = str(guess)
    return guess

def compareToYesterday():
    yesterday = open('yesterday.txt', 'r')
    yesterday = yesterday.read()
    todayGuess = guessNumber()
    while todayGuess == yesterday:
        todayGuess = guessNumber()
        if todayGuess != yesterday:
            break
        else: 
            pass
    overwriteFile(num=todayGuess)
    return todayGuess

def overwriteFile(num):
    overwrite = open('yesterday.txt', 'w')
    overwrite.write(num)
    overwrite.close

def matchName():
    segment = compareToYesterday()
    segment = f'SGMT{segment}'
    file_to_use = None
    for audioFile in glob.glob(f'{folder}\*.wav'):
        if segment in audioFile:
            file_to_use = audioFile
    return  file_to_use

folder = (r'D:\Production\shows\AnimalAir') #path to source files
file_to_use = matchName()

AA = TLShow()
AA.show = 'Animal Airwaves'
AA.show_filename = 'Tenn-AnimalAir'
AA.is_local = True
AA.local_file = file_to_use
AA.check_if_above = 1.1
AA.check_if_below = .9
AA.run()