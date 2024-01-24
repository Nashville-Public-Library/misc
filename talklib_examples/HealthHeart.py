import glob

from talklib.show import TLShow
from talklib.utils import today_is_weekday

def get_file():
    folder = 'D:\Production\shows\HealthHeart'
    try:
        audio_file = glob.glob(f'{folder}\*.wav')
        audio_file = audio_file[0]
    except:
        audio_file = None
    
    return audio_file


def main():
    HH = TLShow()
    HH.show = 'Health in a Heartbeat'
    HH.show_filename = 'Tenn-HealthHeart'
    HH.is_local = True
    HH.local_file = get_file()
    HH.remove_yesterday = False
    HH.remove_source = True
    HH.check_if_above = 2.1
    HH.check_if_below = 1.9
    HH.ffmpeg.compression_level = 18
    HH.run()

if today_is_weekday():
    main()