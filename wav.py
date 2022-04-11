import glob
import sys, os

#this is only needed when converting to an exe file
def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

#this is where the regular program starts
print ("Just a moment...")

for f in glob.glob("*.mp3"):
    origname=(f)
    os.rename(f, "input.mp3")
    os.system("ffmpeg -hide_banner -loglevel quiet -i input.mp3 output.wav")
    #when converting to exe file, change the above line to:
    #os.system(resource_path("ffmpeg -hide_banner -loglevel quiet -i input.mp3 -ar 44100 -ac 1 output.wav"))
    os.rename("output.wav", origname)
    base = os.path.splitext(origname)[0]
    os.rename(origname, base + '.wav')
    os.remove("input.mp3")

for f in glob.glob("*.wav"):
    origname=(f)
    os.rename(f, "input.wav")
    os.system("ffmpeg -hide_banner -loglevel quiet -i input.wav -ac 1 output.wav")
    #when converting to exe file, change the above line to:
    #os.system(resource_path("ffmpeg -hide_banner -loglevel quiet -i input.wav -ar 44100 -ac 1 output.wav"))
    os.rename("output.wav", origname)
    os.remove("input.wav")

os.system("cls")
print ("All done!")
print () #for prettier spacing
input ("(press ENTER to quit)")

    
