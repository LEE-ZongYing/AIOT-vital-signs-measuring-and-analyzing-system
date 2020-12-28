import threading
import pyzenbo
from pyzenbo.modules.dialog_system import RobotFace
from pyzenbo.modules.error_code import code_to_description
import zmq
import time

zenbo_speakSpeed = 100
zenbo_speakPitch = 100
zenbo_speakLanguage = 150
host = '192.168.0.4'
sdk = pyzenbo.connect(host)
domain = 'E7AABB554ACB414C9AB9BF45E7FA8AD9'
timeout = 15
is_looping = True
greeting={}
reponse={}
counter=0

context=zmq.Context()
socket=context.socket(zmq.PULL)
socket.bind("tcp://192.168.0.3:5556")
pusher = context.socket(zmq.PUSH)
pusher.bind("tcp://192.168.0.3:5557")


def CheckDevise(String): # for 體溫、體重、血壓   
    global counter
    length=len(String)
    print(String[length-2:length])
    if String[length-2:length]=='.C':
        counter=1
        greeting[counter]='目前體溫為'+String[0:length-2]+'度,請前往量測體重'
        print(greeting[counter])
    elif String[length-2:length]=='kg':
        counter=2
        greeting[counter]='目前體重為'+String[0:length-2]+'公斤,請前往量測血壓以及血糖'
        print(greeting[counter])
    elif String[length-4:length]=='mmhg':
        counter=3
        half=len(String)/2
        greeting[counter]='目前收縮壓為'+String[0:int(half)-2]+'mmhg、擴張壓為'+String[int(half)-1:length-4]+'mmhg,這是您的網頁並請您拔除健保卡'
        print(greeting[counter])
    elif String=='AllDone':
        counter=100
    return
    
def on_state_change(serial, cmd, error, state):#Called when command state change in waiting queue
    msg = 'on_state_change serial:{}, cmd:{}, error:{}, state:{}'
    print(msg.format(serial, cmd, error, state))
    if error:
        print('on_state_change error:', code_to_description(error))

def CardInput(String):
    global counter
    length=len(String)
    print(String[length-1:length])
    if String[length-1:length]=='M':
        counter=0
        greeting[counter]=String[0:1]+'爺爺您好，請您先量測體溫'
        print('男生')
        if not event_cardinput.isSet():
            event_cardinput.set()
    elif String[length-1:length]=='F':
        counter=0
        greeting[counter]=String[0:1]+'奶奶您好，請您先量測體溫'
        print('女生')
        if not event_cardinput.isSet():
            event_cardinput.set()

def on_result(**kwargs):# Called when a robot command sending result.
    print('on_result', kwargs)


def on_vision(*args):#Called when vision service sending result.
    print('on_vision', args)
    if not event_vision.isSet():
        event_vision.set()


def listen_callback(args): # 收聲音的地方
    print('callbackS')
    slu = args.get('event_slu_query', None)
    if slu and '不需要'==str(slu.get('app_semantic').get('originalSentence')) :
        print(slu)
        def job():
            sdk.robot.set_expression(RobotFace.HAPPY)
            sdk.robot.set_expression(RobotFace.DEFAULT,'好的，若有需要檢測，歡迎再來找我唷', {'speed':zenbo_speakSpeed, 'pitch':zenbo_speakPitch, 'languageId':zenbo_speakLanguage} , sync = True)
        t = threading.Thread(target=job)
        t.start()
    if slu and '需要'==str(slu.get('app_semantic').get('originalSentence')) :
        print(slu)
        def job():
            sdk.robot.set_expression(RobotFace.HAPPY)
            sdk.robot.set_expression(RobotFace.DEFAULT,'那請你先插入健保卡喔', {'speed':zenbo_speakSpeed, 'pitch':zenbo_speakPitch, 'languageId':zenbo_speakLanguage} , sync = True)
        t = threading.Thread(target=job)
        t.start()
        t.join()
        if not event_listen.isSet():
            event_listen.set()
            


def say_hello_and_ask():
    print('say_hello_and_ask')
    sdk.robot.set_expression(RobotFace.HAPPY, timeout=5)
    sdk.robot.jump_to_plan(domain, 'lanuchHelloWolrd_Plan')
    #sdk.robot.speak('你好,我是 Zenbo Junior.')
    sdk.robot.speak_and_listen('需要量測嗎?')
    #需要量測身體狀況，請插入健保卡以便搜尋您的歷史資料哦

def voice():
    print(counter)
    sdk.robot.set_expression(RobotFace.DEFAULT,greeting[counter],{'speed':zenbo_speakSpeed,'pitch':zenbo_speakPitch, 'languageId':zenbo_speakLanguage})
    #zenbo.robot.register_listen_callback(1207, listen_callback)
    time.sleep(int(2))  

def not_found():
    print('not_found')
    sdk.robot.set_expression(RobotFace.HAPPY)
    #sdk.robot.set_expression(RobotFace.DEFAULT, 'Hello,我是Zenbo照護機器人,能夠檢測您目前的健康狀況哦', {'speed':zenbo_speakSpeed, 'pitch':zenbo_speakPitch, 'languageId':zenbo_speakLanguage} , sync = True)
    sdk.robot.set_expression(RobotFace.TIRED, timeout=5)

event_cardinput=threading.Event()
event_vision = threading.Event()
event_listen = threading.Event()
sdk.on_state_change_callback = on_state_change
sdk.on_result_callback = on_result
sdk.on_vision_callback = on_vision
sdk.robot.register_listen_callback(domain, listen_callback)
sdk.robot.set_expression(RobotFace.HIDEFACE, timeout=5)

try:
    while is_looping:
        result = sdk.vision.request_detect_face(enable_debug_preview=True, timeout=50)
        print(result)
        is_detect_face = event_vision.wait(timeout)
        sdk.vision.cancel_detect_face()
        if is_detect_face:
            say_hello_and_ask()#->問候後會自己聽
            is_get_listening = event_listen.wait(timeout)#timeout內有聽到不用謝謝則回覆...，
            
            if is_get_listening:
                print('開始量測')
                event_listen.clear()
                event_vision.clear()
            elif is_get_listening==0:
                print('不用謝謝or沒人')
                event_vision.clear()
                continue
            pusher.send_string("yes")
            CardInfo=socket.recv().decode('utf-8')
            CardInput(CardInfo)
            Is_Card_Input=event_cardinput.wait(timeout)
            CardThread=threading.Thread(target=voice)
            CardThread.start()
            CardThread.join()
            pusher.send_string("yes")
            print('counter = {} '.format(counter))
            while Is_Card_Input and counter!=100: 
                HealthIndicator=socket.recv().decode('utf-8')
                CheckDevise(HealthIndicator)
                robot=threading.Thread(target=voice)
                robot.start()
                robot.join()
                pusher.send_string("yes")
                print('counter = {} '.format(counter))
            event_cardinput.clear()
        else:
            not_found()
        sdk.robot.set_expression(RobotFace.HIDEFACE, timeout=5)
finally:
    sdk.robot.stop_speak_and_listen()
    sdk.vision.cancel_detect_face()
    sdk.release()

