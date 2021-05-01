import threading
import pyzenbo
from pyzenbo.modules.dialog_system import RobotFace
from pyzenbo.modules.error_code import code_to_description
from selenium import webdriver
import zmq
import time

# setting 
zenbo_speakSpeed = 80
zenbo_speakPitch = 110
zenbo_speakLanguage = 150
host = '192.168.0.137'
sdk = pyzenbo.connect(host)
domain = 'E7AABB554ACB414C9AB9BF45E7FA8AD9'
timeout = 30
# is_looping = True
greeting={}
recommandation={}#0:'請問是要量測數據還是想查看網頁呢'
#connection with server
context=zmq.Context()
socket=context.socket(zmq.PULL)
socket.bind("tcp://192.168.0.197:5554")
pusher = context.socket(zmq.PUSH)
pusher.bind("tcp://192.168.0.197:5558")



    
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
    return
def say_hello_and_ask(self):
    print('say_hello_and_ask')
    sdk.robot.set_expression(RobotFace.HAPPY, timeout=2)
    sdk.robot.jump_to_plan(domain, 'lanuchHelloWolrd_Plan')
    SirOrMama=['女士','先生']
    flag=1 if self.unit=='MM' else 0#server幫我篩選過，故比較沒那些難寫   
    sdk.robot.set_expression(RobotFace.DEFAULT,self.MeasureValue+SirOrMama[flag]+'目前量測系統已啟動，請開始量測健康指標',{'speed':zenbo_speakSpeed,'pitch':zenbo_speakPitch, 'languageId':zenbo_speakLanguage})
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
        self.state={0:number_0(),8:number_8(),9:number_9(),10:number_10(),11:number_11(),12:number_12(),13:number_13(),14:number_14(),15:number_15(),99:number_99()}
        self.ATN=int(ATN)
        self.MeasureValue=MeasureValue
        self.unit=unit
    def number_0(self,obj1):#初始狀態，無限開啟人臉辨識就打招呼
        if event_vision.isSet():
            event_vision.clear()
        #if obj1.CheckCardInput(obj1):#怪怪的,呼叫自己的function也把自己傳過去，我想想行不行
        print('開啟相機')
        pusher.send_string("yes")
        result = sdk.vision.request_detect_face(enable_debug_preview=True,timeout=None)
        print('結束相機')
        is_detect_face = event_vision.wait(timeout=21)
        sdk.vision.cancel_detect_face()
        print(is_detect_face)
        if is_detect_face:
            sdk.robot.set_expression(RobotFace.DEFAULT,'您好，我是Zenbo Jr，能給予您一些關於健康上的建議哦，若需要能插入健保卡至讀卡機',{'speed':zenbo_speakSpeed,'pitch':zenbo_speakPitch, 'languageId':zenbo_speakLanguage})
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
        return
    def number_9(self):#Card+pressure
        MessureValueArray=self.MeasureValue.split(',')
        global recommandation
        print(MessureValueArray[0]+'\n'+MessureValueArray[1]+'\n'+MessureValueArray[2])
        greeting[self.ATN]='以偵測到血壓訊號，目前收縮壓為'+MessureValueArray[0]+'mmhg、擴張壓為'+MessureValueArray[1]+'mmhg'+'而心跳每分鐘為'+MessureValueArray[2]+'下'
        self.BloodPressure(MessureValueArray[0],MessureValueArray[1],MessureValueArray[2])
        sdk.robot.set_expression(RobotFace.DEFAULT,greeting[self.ATN]+recommandation[self.ATN],{'speed':zenbo_speakSpeed,'pitch':zenbo_speakPitch, 'languageId':zenbo_speakLanguage})
#       pusher.send_string("yes")
        return 
    def number_12(self):#Card+temperature
        recommandation[self.ATN]=''
        greeting[self.ATN]='以偵測到體溫訊號，目前體溫為'+str(self.MeasureValue)+'度'
        self.ThermoSignal(self.MeasureValue)
        if float(self.MeasureValue)<38.0:
            recommandation[self.ATN]+='請繼續量測體重、血壓，以便讓Zenbo替您做健康分析唷'
        sdk.robot.set_expression(RobotFace.DEFAULT,greeting[self.ATN]+recommandation[self.ATN],{'speed':zenbo_speakSpeed,'pitch':zenbo_speakPitch, 'languageId':zenbo_speakLanguage})
        print(recommandation[self.ATN])
#      pusher.send_string("yes")
        return
    def number_10(self):#Card+weight
        greeting[self.ATN]='以偵測到體重訊號，目前體重為'+str(self.MeasureValue)+'公斤'
        #recommandation[self.ATN]+='能提供Zenbo您的身高嗎? Zenbo能依照身高、體重來建議您如何維持健康哦'
        #如何讓user提供身高
        recommandation[self.ATN]='請繼續量測體溫、血壓，以便讓AI替您做健康分析唷'
        sdk.robot.set_expression(RobotFace.DEFAULT,greeting[self.ATN]+recommandation[self.ATN],{'speed':zenbo_speakSpeed,'pitch':zenbo_speakPitch, 'languageId':zenbo_speakLanguage})
        print(recommandation[self.ATN])
        return
    #-------------------1 phase and 2 phase 分隔線
    def number_11(self):#Card Weight Pressure
        #使用者至第二步，故想查看整體述職的分析結果，說出數值並請使用者測量完。
        flag=1 if self.unit=='kg' else 0
        Device=['血壓計','體重計']
        greeting[self.ATN]='以偵測到'+Device[flag]+'訊號'
        if flag:
            greeting[self.ATN]='以偵測到體重訊號，目前體重為'+str(self.MeasureValue)+'公斤'
            #recommandation[self.ATN]+='能提供Zenbo您的身高嗎? Zenbo能依照身高、體重來建議您如何維持健康哦'
            #如何讓user提供身高
            recommandation[self.ATN]='請繼續量測體溫'
        else:
            MessureValueArray=self.MeasureValue.split(',')
            greeting[self.ATN]='以偵測到血壓訊號，目前收縮壓為'+MessureValueArray[0]+'mmhg、擴張壓為'+MessureValueArray[1]+'mmhg'+'心跳每分鐘'+MessureValueArray[2]+'下'
            self.BloodPressure(MessureValueArray[0],MessureValueArray[1],MessureValueArray[2])
        sdk.robot.set_expression(RobotFace.DEFAULT,greeting[self.ATN]+recommandation[self.ATN],{'speed':zenbo_speakSpeed,'pitch':zenbo_speakPitch, 'languageId':zenbo_speakLanguage})
        print(recommandation[self.ATN])
#      pusher.send_string("yes")
        return
    def number_13(self):# Card Temperature + Pressure
        flag=1 if self.unit=='.C' else 0
        Device=['血壓計','額溫槍']
        greeting[self.ATN]='以偵測到'+Device[flag]+'訊號'
        if flag:
            self.ThermoSignal(self.MeasureValue)
            if float(self.MeasureValue)<=38.0:
                recommandation[self.ATN]+='請繼續量測體重'
        else:
            MessureValueArray=self.MeasureValue.split(',')
            greeting[self.ATN]='以偵測到血壓訊號，目前收縮壓為'+MessureValueArray[0]+'mmhg、擴張壓為'+MessureValueArray[1]+'mmhg'+'而心跳每分鐘為'+MessureValueArray[2]+'下'
            self.BloodPressure(MessureValueArray[0],MessureValueArray[1],MessureValueArray[2])
        sdk.robot.set_expression(RobotFace.DEFAULT,greeting[self.ATN]+recommandation[self.ATN],{'speed':zenbo_speakSpeed,'pitch':zenbo_speakPitch, 'languageId':zenbo_speakLanguage})
        print(recommandation[self.ATN])
        return
    def number_14(self):# Card Temperature +Weight
        flag=1 if self.unit=='kg' else 0
        Device=['額溫槍','體重計']
        greeting[self.ATN]='以偵測到'+Device[flag]+'訊號'
        if flag:
            recommandation[self.ATN]='數值為:'+str(self.MeasureValue)+'公斤,請前往量測血壓及心跳'
        else:
            self.ThermoSignal(self.MeasureValue)
            if float(self.MeasureValue)<38.0:
                recommandation[self.ATN]+='請繼續量測血壓'
        sdk.robot.set_expression(RobotFace.DEFAULT,greeting[self.ATN]+recommandation[self.ATN],{'speed':zenbo_speakSpeed,'pitch':zenbo_speakPitch, 'languageId':zenbo_speakLanguage})
        print(greeting[self.ATN])
    #   pusher.send_string("yes")
        return
    def number_15(self):
        Device=['血壓計','體重計','額溫槍']
        if self.unit=='kg':
            flag=1
        elif self.unit=='hg':
            flag=0
        else:
            flag=2
        greeting[self.ATN]='以偵測到'+Device[flag]+'訊號'
        recommandation[self.ATN]='數值為:'+str(self.MeasureValue)+self.unit
        recommandation[self.ATN]+='全部量測完畢瞜，請拔除健保卡以利Zenbo產生QRcode生成網頁'#此處設定不給建議，建議給網頁上
        sdk.robot.set_expression(RobotFace.DEFAULT,greeting[self.ATN]+recommandation[self.ATN],{'speed':zenbo_speakSpeed,'pitch':zenbo_speakPitch, 'languageId':zenbo_speakLanguage})
        print(greeting[self.ATN])
        return
    def number_99(self):
        print(self.ATN)
        greeting[self.ATN]='想查看歷史量測資料皆可以以手機掃描網頁螢幕上的QRcode'
        #，此外每次的AI分析結果及建議也一併放置在網頁上 recommandation[self.ATN]='感謝您此次的使用，歡迎再次光臨謝謝^^'
        sdk.robot.set_expression(RobotFace.DEFAULT,greeting[self.ATN],{'speed':zenbo_speakSpeed,'pitch':zenbo_speakPitch, 'languageId':zenbo_speakLanguage})
        Server=r'C:\Users\User\Desktop\Designing-implementing-and-testing-an-IoT-based-vital-signs-monitoring-system-for-elderly-health-ca\Code\Zenbo code\selenium\chromedriver.exe'
        driver=webdriver.Chrome(Server)
        driver.get('http://192.168.0.164:8000/qrcode')
        time.sleep(20)
        return
    def BloodPressure(self,SystolicPressure,DiastolicPressure,Beats):
        SPH=True if int(SystolicPressure)>140 else False
        DPH=True if int(DiastolicPressure)>90 else False
        if SPH==False:#收縮
            if DPH:
                recommandation[self.ATN]='舒張血壓偏高、收縮血壓偏低，最近工作很勞累喔，請多多活動身體，讓自己喘口氣吧'#若有任何問題歡迎在量測一次，建議能左右手血壓各量測一次，分析結果會更為準確喔
            else:
                if(int(SystolicPressure)<100):
                    recommandation[self.ATN]='血壓過低小心有休克的危機喔，請密切觀察盡早處理。'
                else:
                    recommandation[self.ATN]='恭喜你血壓沒有問題，請保持目前的生活作息，能使你更有活力喔。'
        else:
            if DPH:#舒張
                recommandation[self.ATN]='收縮血壓、擴張血壓數據偏高，勞煩您近期多注意自己的身體，有需要能前往醫院進行更精密的檢查'#，若出現頭暈、噁心、嘔吐現象請馬上前往醫院進行檢查
            else:
                recommandation[self.ATN]='舒張血壓偏高、收縮血壓偏高，請養成運動習慣，每次20到30分鐘，能幫您降低血壓喔'
        return
    def ThermoSignal(self,BodyTemp):
        if float(BodyTemp)>38.0:
            recommandation[self.ATN]='您的體溫過高瞜，為了您及Zenbo的健康請一同戴上口罩八，此外，若身體有任何不適請盡速前往醫院'
        elif float(BodyTemp)>=37.0:
                recommandation[self.ATN]='體溫稍高，若有運動、跑跳皆為正常現象'
        elif float(BodyTemp)>=36.0:
                recommandation[self.ATN]='體溫在正常範圍內，但請不要忘記戴口罩防範Covid Nineteen喔'
        elif float(BodyTemp)<35.0:
                recommandation[self.ATN]='體溫不太正常，請將額頭靠近額溫槍'
        return
    # def CheckCardInput(self,IsObj1):
    #     try:
    #         string = socket.recv(flags=zmq.NOBLOCK)
    #         if string[0:2]=='08':
    #             print('Ready go to face recognition but CardInput happen.')
                
    #             return True
    #     except zmq.Again as e:
    #         return False
class number_0(object):
    def exec(self,obj1):
        obj1.number_0(obj1)
        return
    def exit(self):
        pass
class number_8(number_0):
    def exec(self,obj1):
        obj1.number_8()        
        return
    def exit(self):
        pass
class number_9(number_8):
    def exec(self,obj1):
        print('start')
        obj1.number_9()
        return
    def exit(self):
        pass
class number_12(object):
    def exec(self,obj1):
        obj1.number_12()
        return
    def exit(self):
        pass
class number_10(object):
    def exec(self,obj1):
        obj1.number_10()
        return
    def exit(self):   
        pass
class number_11(object):
    def exec(self,obj1):
        obj1.number_11()
        return
    def exit(self):
        pass
class number_13(number_0):
    def exec(self,obj1):
        obj1.number_13()
        return
class number_14(object):
    def exec(self,obj1):
        obj1.number_14()
        return
    def exit(self):
        pass    
class number_15(object):
    def exec(self,obj1):
        obj1.number_15()
        return
    def exit(self):
        pass
class number_99(object):
    def exec(self,obj1):
        obj1.number_99()
        return
    def exit(self):
        pass
def run(RawData):
    print(RawData)
    Case=Switcher((lambda x:x[0:2])(RawData),(lambda x:x[2:len(x)-2])(RawData),(lambda x:x[len(x)-2:len(x)])(RawData))#改成用,分隔數值會比較好找
    fsm=Case.state[Case.ATN]
    fsm.exec(Case)
    print(RawData,Case)
    return

event_cardinput=threading.Event()
event_vision = threading.Event()
event_listen = threading.Event()
sdk.on_state_change_callback = on_state_change
sdk.on_result_callback = on_result
sdk.on_vision_callback = on_vision
sdk.robot.register_listen_callback(domain, listen_callback)
sdk.robot.set_expression(RobotFace.HIDEFACE, timeout=5)

try:
    while True:
        RawData=socket.recv().decode('utf-8')
        run(RawData)

finally:
    sdk.robot.stop_speak_and_listen()
    sdk.vision.cancel_detect_face()
    sdk.release()