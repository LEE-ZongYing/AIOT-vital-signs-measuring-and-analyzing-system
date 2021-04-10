import pyzenbo
import pyzenbo.modules.zenbo_command as commands
import time
from pyzenbo.modules.dialog_system import RobotFace
zenbo_speakSpeed = 100
zenbo_speakPitch = 100
zenbo_speakLanguage = 1
zenbo = pyzenbo.connect('192.168.43.240')
print("執行")
zenbo.media.play_media('','IMG_20210327_165646.jpg')# 您需要將檔案放在裝置中指定的路徑 /sdcard/Zenbo實驗室/
time.sleep(10)
exit()