import os
import shutil

def generateVideo(folder):
    print("\n---------- generating video ----------")
    
    shutil.copy('../assest/z1.jpg', './{folder}/'.format(folder=folder))
    shutil.copy('../assest/z2.jpg', './{folder}/'.format(folder=folder))
    
    os.system("ffmpeg -framerate 1/6 -pattern_type glob -i './{folder}/*.jpg' -c:v libx264 -crf 25 -r 30 -pix_fmt yuv420p -s 720x480 './{folder}/temp.mp4'".format(folder=folder))
    os.system("ffmpeg -i './{folder}/temp.mp4' -i ../assest/background-sound.mp3 -map 0 -map 1:a -c:v copy -shortest './{folder}/{folder}.mp4'".format(folder=folder))
    
    os.remove("./{folder}/z1.jpg".format(folder=folder))
    os.remove("./{folder}/z2.jpg".format(folder=folder))
    os.remove("./{folder}/temp.mp4".format(folder=folder))