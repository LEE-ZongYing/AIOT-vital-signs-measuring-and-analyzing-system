import pyzenbo
from pyzenbo.modules.dialog_system import RobotFace
from pyzenbo.modules import vision_control
import threading 
import time 

host = '192.168.0.60'
sdk = pyzenbo.connect(host)
#result={'a':'dict'}

def T2_job():
    sdk.robot.set_expression(RobotFace.SHOCKED, 'Hello World')
    sdk.robot.set_expression(RobotFace.HIDEFACE)
    try:
        while(1):
            result = sdk.vision.wait_for_detect_face(interval=1.5,enable_debug_preview=True,enable_candidate_obj=True,timeout=20)
            if result==None:
                print('continue')
                continue
            elif isinstance(result,dict):
                sdk.vision.cancel_detect_face()
                continue
            elif isinstance(result,list):
                print(result)
                break 
            # elif isinstance(result,list):
            #     print('1')
            #     break
    finally:
        print('2')
        time.sleep(3)#要睡一下在多連結下，連線要慢慢關
        sdk.media.stop_media()
        time.sleep(3)
        sdk.release()



def main():
    added_thread=threading.Thread(target=T2_job,name='均') 
    # print(threading.active_count()) #算有多少被激活的threa8d
    # print(threading.enumerate())
    # print(threading.current_thread())
    added_thread.start()
    added_thread.join()
    print('hello')


if __name__=='__main__':
    main()

