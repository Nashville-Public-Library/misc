from talklib.show import TLShow
from datetime import datetime
import glob

show = 'Bird Note' # for notifications
output_file = 'Tenn-BirdNote.wav' #name of file with .wav extension
folder = (r'C:\Users\wrprod\Desktop\BirdNote') #path to source files

#TODO: explain what this is doing!
def matchName():
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
    file_to_use = None
    for file in glob.glob(f'{folder}\*.wav'):
        if sgmt in file:
            file_to_use = file
    return file_to_use

folder = r'D:\Production\shows\BirdNote'
file_to_use = matchName()

BN = TLShow()
BN.show = 'Bird Note'
BN.show_filename = 'Tenn-BirdNote'
BN.is_local = True
BN.local_file = file_to_use
BN.check_if_above = 1.76
BN.check_if_below = 1.74
BN.remove_source = True
BN.run()