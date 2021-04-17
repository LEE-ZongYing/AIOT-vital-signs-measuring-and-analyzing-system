import pyzenbo
import pyzenbo.modules.zenbo_command as commands
import time
from pyzenbo.modules.dialog_system import RobotFace
zenbo_speakSpeed = 100
zenbo_speakPitch = 100
zenbo_speakLanguage = 1
zenbo = pyzenbo.connect('192.168.43.50')
timeout=30

def historical_record():
    zenbo.robot.set_expression(RobotFace.DEFAULT,'這是您的QRCode', {'speed':zenbo_speakSpeed, 'pitch':zenbo_speakPitch, 'languageId':zenbo_speakLanguage})
    zenbo.media.play_media('', 'IMG_20210414_135223.jpg', sync=)

    time.sleep(5)
    exit()
historical_record()
zenbo.media.stop_media()
zenbo.release()