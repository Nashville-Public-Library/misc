from talklib.show import TLShow
import glob
from datetime import datetime


def matchName():
    '''TODO explain this'''
    dict = {
    'Mon': 'SGMT01',
    'Tue': 'SGMT02',
    'Wed': 'SGMT03',
    'Thu': 'SGMT04',
    'Fri': 'SGMT05'
    }
    
    file_to_use = None
    day_abbr = datetime.now().strftime("%a")
    sgmt = dict.get(day_abbr)
    files = glob.glob(f'{folder}\*.wav')
    for file in files:
        if sgmt in file:
            file_to_use = file

    return  file_to_use
    
folder = r'D:\Production\shows\SoundBeat'
file_to_use = matchName()

SB = TLShow()
SB.show = 'Sound Beat'
SB.show_filename = 'Tenn-SoundBeat'
SB.is_local = True
SB.local_file = file_to_use
SB.remove_source = True
SB.check_if_above = 1.51
SB.check_if_below = 1.49
SB.run()
