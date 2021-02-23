import threading
import pyzenbo
from pyzenbo.modules.dialog_system import RobotFace
from pyzenbo.modules.error_code import code_to_description
import zmq
import time

# setting 
zenbo_speakSpeed = 100
zenbo_speakPitch = 100
zenbo_speakLanguage = 150
host = '192.168.0.4'
sdk = pyzenbo.connect(host)
domain = 'E7AABB554ACB414C9AB9BF45E7FA8AD9'
timeout = 15
is_looping = True
greeting={}
recommandation={}#0:'請問是要量測數據還是想查看網頁呢'
counter=0
#connection with server
context=zmq.Context()
socket=context.socket(zmq.PULL)
socket.bind("tcp://192.168.0.3:5556")
pusher = context.socket(zmq.PUSH)
pusher.bind("tcp://192.168.0.3:5557")

event_cardinput=threading.Event()
event_vision = threading.Event()
event_listen = threading.Event()
sdk.on_state_change_callback = on_state_change
sdk.on_result_callback = on_result
sdk.on_vision_callback = on_vision
sdk.robot.register_listen_callback(domain, listen_callback)
sdk.robot.set_expression(RobotFace.HIDEFACE, timeout=5)

    
def on_state_change(serial, cmd, error, state):#Called when command state change in waiting queue
    msg = 'on_state_change serial:{}, cmd:{}, error:{}, state:{}'
    print(msg.format(serial, cmd, error, state))
    if error:
        print('on_state_change error:', code_to_description(error))

def on_result(**kwargs):# Called when a robot command sending result.
    print('on_result', kwargs)


def on_vision(*args):#Called when vision service sending result.
    print('on_vision', args)
    if not event_vision.isSet():
        event_vision.set()


def listen_callback(args):
    print('callbackS')
    slu = args.get('event_slu_query', None)
    if slu and '量測指標'==str(slu.get('app_semantic').get('originalSentence')) :
        print(slu)
        def job():
            sdk.robot.set_expression(RobotFace.HAPPY)
            sdk.robot.set_expression(RobotFace.DEFAULT,'好的，那請您前往量測儀器進行測量哦', {'speed':zenbo_speakSpeed, 'pitch':zenbo_speakPitch, 'languageId':zenbo_speakLanguage} , sync = True)
        t = threading.Thread(target=job)
        t.start()
        if not event_listen.isSet():
            event_listen.set()
            #此時使用者會插入健保卡、State become CardOnly from initialState
    elif slu and '查看資料'==str(slu.get('app_semantic').get('originalSentence')) :
        print(slu)
        def job():
            sdk.robot.set_expression(RobotFace.HAPPY)
            sdk.robot.set_expression(RobotFace.DEFAULT,'這是您的QRCode', {'speed':zenbo_speakSpeed, 'pitch':zenbo_speakPitch, 'languageId':zenbo_speakLanguage} , sync = True)
            zenbo.media.play_media('', 'IMG_20201025_193919.jpg', sync=True,timeout=100)#
        t = threading.Thread(target=job)
        t.start()
        t.join()


def say_hello_and_ask(self):
    print('say_hello_and_ask')
    sdk.robot.set_expression(RobotFace.HAPPY, timeout=5)
    sdk.robot.jump_to_plan(domain, 'lanuchHelloWolrd_Plan')
    SirOrMama=['先生','女士']
    flag=1 if self.unit=='MM' else 0#server幫我篩選過，故比較沒那些難寫   
    sdk.robot.speak_and_listen(self.MeasureValue+SirOrMama[flag]+'你好,我是 Zenbo Junior，請問您想量測指標或是查看歷史資料呢?',timeout=5)
    #需要量測身體狀況，請插入健保卡以便搜尋您的歷史資料哦


def voice():
    print(counter)
    sdk.robot.set_expression(RobotFace.DEFAULT,greeting[counter],{'speed':zenbo_speakSpeed,'pitch':zenbo_speakPitch, 'languageId':zenbo_speakLanguage})
    zenbo.robot.register_listen_callback(1207, listen_callback)
    time.sleep(int(2))  

def not_found():
    print('not_found')
    sdk.robot.set_expression(RobotFace.HAPPY)
    #sdk.robot.set_expression(RobotFace.DEFAULT, 'Hello,我是Zenbo照護機器人,能夠檢測您目前的健康狀況哦', {'speed':zenbo_speakSpeed, 'pitch':zenbo_speakPitch, 'languageId':zenbo_speakLanguage} , sync = True)
    sdk.robot.set_expression(RobotFace.TIRED, timeout=5)

class Switcher(object):#state switcher 
    def __init__(self,ATN,MeasureValue,unit):
        self.method_name='number_'+str(ATN)
        self.method=self.getattr(self, method_name,'NO')
        self.ATN=ATN
        self.MeasureValue=MeasureValue
        self.unit=unit
        return self.method_name
    def number_0(self):#初始狀態，無限開啟人臉辨識就打招呼
        result = sdk.vision.request_detect_face(enable_debug_preview=True, timeout=50)
        print(result)
        is_detect_face = event_vision.wait(timeout)
        sdk.vision.cancel_detect_face()
        if is_detect_face:
            sdk.robot.set_expression(RobotFace.DEFAULT,'您好，我是您的健康監控小幫手Zenbo，對健康有疑問都能夠來找我喔',{'speed':zenbo_speakSpeed,'pitch':zenbo_speakPitch, 'languageId':zenbo_speakLanguage})
            #被直接詢問專業知識
   #     pusher.send_string("yes")
        return
    def number_8(self):#onlyCard
        say_hello_and_ask(self)#->問候後會自己聽
        is_get_listening = event_listen.wait(timeout)#timeout內有聽到不用謝謝則回覆...，
        if is_get_listening:
            print('有人要量測數據')
            event_listen.clear()
        else:
            print('不用謝謝or沒人or叫出網頁or沒有語音辨識到，但有卡片')
    #    pusher.send_string("yes")
        return 'Yes'
    def number_9(self):#Card+pressure
        MessureValueArray=self.MeasureValue.split(',')
        global recommandation[self.ATN]=''
        greeting[self.ATN]='以偵測到血壓訊號，目前收縮壓為'+MessureValueArray[0]+'mmhg、擴張壓為'+MessureValueArray[1]+'mmhg'+'心跳每分鐘'+MessureValueArray[2]+'下'
        SPH=True if systolicBP>140 else False
        DPH=True if DiastolicBP>90 else False
        if SPH==False:
            if DPH:
                recommandation[self.ATN]='目前舒張壓偏高喔，若有任何問題歡迎在量測一次，建議能左右手血壓各量測一次，分析結果會更為準確喔'
            else:
                {
                    recommandation[self.ATN]='恭喜你還非常的健康喔，保持目前的生活作息，能使你更有活力喔。'
                }
        else:{
            if DPH:
                recommandation[self.ATN]='收縮血壓、擴張血壓數據偏高，勞煩您近期多注意自己的身體，若出現頭暈、噁心、嘔吐現象請馬上前往醫院進行檢查'
        }
        recommandation+='請繼續量測體溫、體重以便讓Zenbo Junior繼續替您做更詳細的健康分析哦'
        print(recommandation[counter])
        sdk.robot.set_expression(RobotFace.DEFAULT,greeting[self.ATN]+recommandation[self.ATN],{'speed':zenbo_speakSpeed,'pitch':zenbo_speakPitch, 'languageId':zenbo_speakLanguage})
 #       pusher.send_string("yes")
        return 'Yes'
    def number_12(self):#Card+temperature
        RealNumber=double(self.MeasureValue)
        recommandation[self.ATN]=''
        greeting[self.ATN]='以偵測到體溫訊號，目前體溫為'+str(self.MeasureValue)+'度,請繼續量測體重、血壓以便讓AI替您做健康分析唷'
        flag = True if RealNumber>38.0 else False :
        if flag:
            recommandation[self.ATN]='您的體溫過高瞜，為了您以及Zenbo的健康請一同戴上口罩八，此外如果身體有任何不適請盡速前往醫院'
        else:
            if RealNumber>37.0:
                recommandation[self.ATN]='體溫稍高，若有運動、跑跳皆為正常現象，想再次確認體溫，歡迎過1至2分鐘後，再次回來做量測'
        sdk.robot.set_expression(RobotFace.DEFAULT,greeting[self.ATN]+recommandation[self.ATN],{'speed':zenbo_speakSpeed,'pitch':zenbo_speakPitch, 'languageId':zenbo_speakLanguage})
        print(recommandation[self.ATN])
  #      pusher.send_string("yes")
        return
    def number_10(self):#Card+weight
        
        recommandation[self.ATN]='以偵測到體重訊號，目前體重為'+str(self.MeasureValue)+'公斤,請繼續量測體溫、血壓，以便讓AI替您做健康分析唷'
        recommandation[self.ATN]+='能提供Zenbo您的身高嗎? Zenbo能依照身高、體重來建議您如何維持健康哦'
        #如何讓user提供身高
        sdk.robot.set_expression(RobotFace.DEFAULT,recommandation[self.ATN],{'speed':zenbo_speakSpeed,'pitch':zenbo_speakPitch, 'languageId':zenbo_speakLanguage})
        print(recommandation[self.ATN])
 #       pusher.send_string("yes")
        return'Yes'
    #-------------------1 phase and 2 phase 分隔線
    def number_11(self):#Card Weight Pressure
        #使用者至第二步，故想查看整體述職的分析結果，說出數值並請使用者測量完。
        flag=1 if self.unit='kg' else =0
        if flag:
            recommandation[self.ATN]='以量測到體重計訊號，數值為:'+str(self.ATN)+'請前往量測下一生理指標。'
        else:
            recommandation[self.ATN]='以量測到血壓計訊號，數值為:'+str(self.ATN)+'請前往量測下一生理指標。'
        sdk.robot.set_expression(RobotFace.DEFAULT,recommandation[self.ATN],{'speed':zenbo_speakSpeed,'pitch':zenbo_speakPitch, 'languageId':zenbo_speakLanguage})
        print(recommandation[self.ATN])
  #      pusher.send_string("yes")
        return'Yes'
    def ChangeState(self,NewATN)
        if NewATN == self.ATN:
            self.method_name='number_'+str(ATN)
            self.method=self.getattr(self, method_name,'NO')
    def number_13(self):# Card Temperature + Pressure
        flag=1 if self.unit='hg' else =0
        if flag:
            recommandation[self.ATN]='以量測到血壓計訊號，數值為:'+str(self.ATN)+'請前往量測下一生理指標。'
        else:
            recommandation[self.ATN]='以量測到額溫槍訊號，數值為:'+str(self.ATN)+'請前往量測下一生理指標。'
        sdk.robot.set_expression(RobotFace.DEFAULT,recommandation[self.ATN],{'speed':zenbo_speakSpeed,'pitch':zenbo_speakPitch, 'languageId':zenbo_speakLanguage})
        print(recommandation[self.ATN])
        return'Yes'
    def number_14(self):# Card Temperature +Weight
        flag=1 if self.unit='kg' else =0
        if flag:
            recommandation[self.ATN]='以量測到體重計訊號，數值為:'+str(self.ATN)+'請前往量測下一生理指標。'
        else:
            recommandation[self.ATN]='以量測到額溫槍訊號，數值為:'+str(self.ATN)+'請前往量測下一生理指標。'
        sdk.robot.set_expression(RobotFace.DEFAULT,recommandation[self.ATN],{'speed':zenbo_speakSpeed,'pitch':zenbo_speakPitch, 'languageId':zenbo_speakLanguage})
        print(recommandation[self.ATN])
     #   pusher.send_string("yes")
        return'Yes'
    def number_15(self):
        greeting[self.ATN]='生理指標量測完畢'
        recommandation[self.ATN]='這邊是您此次量測數值的紀錄，想查看歷史量測資料皆可以以手機掃描下方QRcode，by the way 每次AI分析數據、結果也會一併放置在網頁上'
        zenbo.media.play_media('', 'IMG_20201025_193919.jpg', sync=True,timeout=100)#
  #      pusher.send_string("yes")
        return'Yes'
        #秀出網頁+QRcode
        #Zenbo : 。
class number_0(object):
    def __init__(self,obj1):
        obj1.number_0
    def exit(self):
class number_8(number_0):
    def __init__(self,obj1):
        obj1.number_8
        return
    def exit(self):
class number_9(number_8):
    def __init__(self,obj1):
        obj1.method
    def exit(self):
class number_12(object):
    def __init__(self,obj1):
        obj1.method
    def exit(self):
class number_10(object):
    def __init__(self,obj1):
        obj1.method
    def exit(self):          
class number_11(object):
    def __init__(self,obj1):
        obj1.method
    def exit(self):
        pass
class number_13(number_0):
    def __init__(self,obj1):
        obj1.CTM()
class number_14(object):
    def __init__(self,obj1):
        obj1.method
    def exit(self):    
class number_15(object):
    def __init__(self,obj1):
        obj1.method
    def exit(self):


def run():
    RawData=socket.recv().decode('utf-8')
    sm=StateManager()
    
    Case=Switcher((lambda x:x[0:2])(RawData),(lambda x:x[2:len(x)-2])(RawData),(lambda x:x[len(x)-2:len(x)])(RawData))#改成用,分隔數值會比較好找
    print(Case)
    pusher.send_string("yes")
class StateManager(object):
    def changeState(self, NewState, objs):
        for obj in objs:
            #   如果新產生的訊號和物件原本的執行狀態對應的訊號一致的話
            print('目前狀態為： {}'.format(obj1.state))
            if NewState == obj.state:
                #   保持原狀態
                fsm = self.getFsm(obj.state)
                fsm.exec(obj)
            else:
                #   先退出舊狀態
                old_fsm = self.getFsm(obj.state)
                old_fsm.exit(obj)
                #   執行新狀態
                obj.state = NewState
                new_fsm = self.getFsm(NewState)
                new_fsm.exec(obj)
                if 15 == obj1.state:
                    return
try:
    while True:
        run()
finally:
    sdk.robot.stop_speak_and_listen()
    sdk.vision.cancel_detect_face()
    sdk.release()


