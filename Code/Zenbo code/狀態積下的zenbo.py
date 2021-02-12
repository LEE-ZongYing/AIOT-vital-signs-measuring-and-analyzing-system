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
    if slu and '量測數據'==str(slu.get('app_semantic').get('originalSentence')) :
        print(slu)
        def job():
            sdk.robot.set_expression(RobotFace.HAPPY)
            sdk.robot.set_expression(RobotFace.DEFAULT,'好的，那請您先插入健保卡確認身分唷', {'speed':zenbo_speakSpeed, 'pitch':zenbo_speakPitch, 'languageId':zenbo_speakLanguage} , sync = True)
        t = threading.Thread(target=job)
        t.start()
        if not event_listen.isSet():
            event_listen.set()
            #此時使用者會插入健保卡、State become CardOnly from initialState
    elif slu and '查看網頁'==str(slu.get('app_semantic').get('originalSentence')) :
        print(slu)
        def job():
            sdk.robot.set_expression(RobotFace.HAPPY)
            sdk.robot.set_expression(RobotFace.DEFAULT,'這是您的QRCode', {'speed':zenbo_speakSpeed, 'pitch':zenbo_speakPitch, 'languageId':zenbo_speakLanguage} , sync = True)
            #螢幕跳出QRcode
        t = threading.Thread(target=job)
        t.start()
        t.join()


def say_hello_and_ask(self):
    print('say_hello_and_ask')
    sdk.robot.set_expression(RobotFace.HAPPY, timeout=5)
    sdk.robot.jump_to_plan(domain, 'lanuchHelloWolrd_Plan')
    SirOrMama=['先生','女士']
    flag=1 if self.unit=='MM' else 0#server幫我篩選過，故比較沒那些難寫
    if flag:    
        sdk.robot.speak_and_listen(self.MeasureValue+SirOrMama[flag]+'你好,我是 Zenbo Junior，請問您想量測生理指標或是查看歷史資料網頁呢?')
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
    def number_0(self):#無限開啟While看到人就打招呼
        result = sdk.vision.request_detect_face(enable_debug_preview=True, timeout=50)
        print(result)
        is_detect_face = event_vision.wait(timeout)
        sdk.vision.cancel_detect_face()
        if is_detect_face:
            sdk.robot.set_expression(RobotFace.DEFAULT,'您好，我是您的健康監控小幫手Zenbo，對健康有疑問都能夠來找我喔',{'speed':zenbo_speakSpeed,'pitch':zenbo_speakPitch, 'languageId':zenbo_speakLanguage})
            #被直接詢問專業知識
            pusher.send_string("yes")
    def number_8(self):#onlyCard
        #ask measure or check web語音辨識
        say_hello_and_ask(self)#->問候後會自己聽
        is_get_listening = event_listen.wait(timeout)#timeout內有聽到不用謝謝則回覆...，
        if is_get_listening:
            print('有人要量測數據，已請她插入健保卡')
            event_listen.clear()
            event_vision.clear()
        elif is_get_listening==0:
            print('不用謝謝or沒人or叫出網頁')
            event_vision.clear()
        CardThread=threading.Thread(target=voice)
        CardThread.start()
        CardThread.join()
        pusher.send_string("yes")
        print('counter = {} '.format(counter))
    def number_9():#Card+pressure
        systolicBP=(String[0:int(half)-2])
        DiastolicBP=String[int(half)-1:length-4]
        greeting[counter]='以偵測到血壓訊號，目前收縮壓為'+String[0:int(half)-2]+'mmhg、擴張壓為'+String[int(half)-1:length-4]+'mmhg'+'心跳每分鐘'+String[xx]+'下'
        if systolicBP>140:
            recommandation[counter]='目前收縮壓偏高'
            if DiastolicBP >90:
                recommandation[counter]+='及舒張壓偏高，若有任何劇烈頭痛、嘔吐、四肢無力等現象，建議前往醫院做詳細的檢查，以確保自身健康沒有問題哦' 
        #如何知道上之手的數值(左右手)
        #程式預測，分數高就1中2低3
        print(greeting[counter])
    def number_12():#Card+temperature
        recommandation[counter]=''
        RealNumber=float(String[0:length-2])
        greeting[counter]='以偵測到體溫訊號，目前體溫為'+str(RealNumber)+'度,請繼續量測體重、血壓以便讓AI替您做健康分析唷'
        flag = True if RealNumber>38.0 else False :
        if flag:
            recommandation[counter]='您的體溫過高瞜，為了您以及Zenbo的健康請一同戴上口罩八，此外如果身體有任何不適請盡速前往醫院'
        else:
            if RealNumber>37.0:
                recommandation[counter]='體溫稍高，若有運動、跑跳接為正常現象，想再次確認體溫，歡迎過1至2分鐘後，再次回來做量測'
        print(recommandation[counter])#CheckPoint
    def number_10():#Card+weight
        greeting[counter]='以偵測到體重訊號，目前體重為'+String[0:length-2]+'公斤,請繼續量測體溫、血壓，以便讓AI替您做健康分析唷'
        #recommandation[counter]='能提供Zenbo您的身高嗎? Zenbo能依照身高、體重來建議您如何維持健康'
        #如何讓user提供身高
        print(greeting[counter])
    #-------------------1 phase and 2 phase 分隔線
    def number_11():#Card Weight Pressure
        #使用者至第二步，故想查看整體述職的分析結果，說出數值並請使用者測量完。
    def number_13():# Card Temperature + Pressure
    def number_14():# Card Temperature +Weight
        else:
            print('CardReadProblem -->> Measurement not ')
        return

class number_0(object):#全0時初始狀態
    def __init__(self,obj1):
        obj1.number_0

    def exit(self):
        pass
class CTM(State):
    def NoticeRobot(self,obj1):
        obj1.CTM()
    # @property
    # def s(self, )
    
    # def get_value(self,)

    # def send(self, unit):
    #     pass



def run():
    RawData=socket.recv().decode('utf-8')
    Case=Switcher((lambda x:x[0:2])(RawData),(lambda x:x[2:len(x)-2])(RawData),(lambda x:x[len(x)-2:len(x)])(RawData))
    print(Case)#CheckPoint
    cas.exec()
    Is_Card_Input=event_cardinput.wait(timeout)
    CardThread=threading.Thread(target=voice)
    CardThread.start()
    CardThread.join()
    pusher.send_string("yes")
    print('counter = {} '.format(counter))

try:
    while is_looping:
            CardThread=threading.Thread(target=voice)
            CardThread.start()
            CardThread.join()
            pusher.send_string("yes")
            print('counter = {} '.format(counter))
            while Is_Card_Input and counter!=100: 
                HealthIndicator=socket.recv().decode('utf-8')
                CheckDevise(HealthIndicator)
                exec()
                print('counter = {} '.format(counter))
            event_cardinput.clear()
        else:
            not_found()
        sdk.robot.set_expression(RobotFace.HIDEFACE, timeout=5)
finally:
    sdk.robot.stop_speak_and_listen()
    sdk.vision.cancel_detect_face()
    sdk.release()

event_cardinput=threading.Event()
event_vision = threading.Event()
event_listen = threading.Event()
sdk.on_state_change_callback = on_state_change
sdk.on_result_callback = on_result
sdk.on_vision_callback = on_vision
sdk.robot.register_listen_callback(domain, listen_callback)
sdk.robot.set_expression(RobotFace.HIDEFACE, timeout=5)