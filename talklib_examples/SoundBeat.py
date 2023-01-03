from talklib.show import TLShow
from talklib.utils import today_is_weekday
import glob
from datetime import datetime


def matchName():
    '''TODO explain this'''
    folder = r'D:\Production\shows\SoundBeat'

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

def main():
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

if today_is_weekday():
    main()