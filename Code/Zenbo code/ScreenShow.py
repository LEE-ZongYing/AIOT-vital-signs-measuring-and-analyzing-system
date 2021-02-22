import pyzenbo
import pyzenbo.modules.zenbo_command as commands
import time
from pyzenbo.modules.dialog_system import RobotFace
zenbo_speakSpeed = 100
zenbo_speakPitch = 100
zenbo_speakLanguage = 1
zenbo = pyzenbo.connect('192.168.43.239')

def event__E5_9C_96_E5_BD_A2_E4_BB_8B_E9_9D_A21__E9_A0_81_E9_9D_A21__E9_A0_85_E7_9B_AE3_Withdraw_Card_from_CardReader():
    zenbo.robot.set_expression(RobotFace.DEFAULT, '歡迎下次再來找Zenbo紀錄生理指標唷', {'speed':zenbo_speakSpeed, 'pitch':zenbo_speakPitch, 'languageId':zenbo_speakLanguage} , sync = True)

def historical_record():
    zenbo.robot.set_expression(RobotFace.DEFAULT,'您好，我是您的健康監控小幫手Zenbo，對健康有疑問都能夠來找我喔',{'speed':zenbo_speakSpeed,'pitch':zenbo_speakPitch, 'languageId':zenbo_speakLanguage})
    zenbo.media.play_media('', 'IMG_20201025_193919.jpg', sync=True,timeout=100)# 您需要將檔案放在裝置中指定的路徑 /sdcard/Zenbo實驗室/
    time.sleep(int(1))
    time.sleep(int(10))
def event__E5_9C_96_E5_BD_A2_E4_BB_8B_E9_9D_A21__E9_A0_81_E9_9D_A21__E9_A0_85_E7_9B_AE1_Measure_Vital_Signs():
    zenbo.robot.set_expression(RobotFace.DEFAULT, '已同步到其他量測裝置，請開始今天的量測', {'speed':zenbo_speakSpeed, 'pitch':zenbo_speakPitch, 'languageId':zenbo_speakLanguage} , sync = True)

zenbo.robot.set_expression(RobotFace.DEFAULT)
historical_record()
time.sleep(int(10))



zenbo.media.stop_media()
zenbo.release()