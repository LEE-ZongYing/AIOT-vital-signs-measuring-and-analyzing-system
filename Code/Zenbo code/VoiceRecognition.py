import pyzenbo
import pyzenbo.modules.zenbo_command as commands
import time
from pyzenbo.modules.dialog_system import RobotFace
import threading
from pyzenbo.modules.error_code import code_to_description
import zmq




zenbo_speakSpeed = 100
zenbo_speakPitch = 100
zenbo_speakLanguage = 100
is_looping = True
timeout = 15
greeting={}
'''1:'Hello ， 我是zenbo，體溫正常，請前往測量體重喔',2:'溫度有點偏高，可能發燒摟，請繼續前往量測體重喔',3:'量測到體重瞜 ， 請前往量測血壓',
4:'三項健康指標都量測完成搂，這是您的數據'
'''
'''
0:'第一站為額溫槍，請將額頭靠近額溫槍 '
1:'正在搜尋有無量測到體重...',2:'正在搜尋有無量測到體重...',3:'正在搜尋有無量測到血壓',4:'歡迎需要任何建議都可以來找我哦'
'''
counter=0
reponse={}

#ValueSuggestion={1:'目前有點發燒，在人潮眾多的地方請記得戴上口罩哦',2:''}
try :
    sdk='192.168.0.60'
    zenbo = pyzenbo.connect(sdk)
except:
    print('沒連到')
    
# context=zmq.Context()
# socket=context.socket(zmq.PULL)
# socket.bind("tcp://192.168.0.11:5556")
# pusher = context.socket(zmq.PUSH)
# pusher.bind("tcp://192.168.0.11:5557")


def listen_callback(args):
    event_slu_query = args.get('event_slu_query', None)
    if event_slu_query and '是的我想量測' == str(event_slu_query.get('app_semantic').get('originalSentence')):    
        print('start job')
        def job():
            zenbo.robot.set_expression(RobotFace.HAPPY)
            zenbo.robot.set_expression(RobotFace.DEFAULT,reponse[counter], {'speed':zenbo_speakSpeed, 'pitch':zenbo_speakPitch, 'languageId':zenbo_speakLanguage} , sync = True)
        t = threading.Thread(target=job)
        t.start()
    event_slu_query = args.get('event_slu_query', None)
    if event_slu_query and'不需要謝謝' == str(event_slu_query.get('app_semantic').get('originalSentence')):
            zenbo.robot.set_expression(RobotFace.HAPPY)
            zenbo.robot.set_expression(RobotFace.DEFAULT, '好的，有其他問題歡迎回來找我喔', {'speed':zenbo_speakSpeed, 'pitch':zenbo_speakPitch, 'languageId':zenbo_speakLanguage} , sync = True)

def not_found():
    print('value error ')
    zenbo.robot.set_expression(RobotFace.TIRED)

def voice():
    print(counter)
    zenbo.robot.set_expression(RobotFace.DEFAULT,greeting[counter],{'speed':zenbo_speakSpeed,'pitch':zenbo_speakPitch, 'languageId':zenbo_speakLanguage})
    #zenbo.robot.register_listen_callback(1207, listen_callback)
    time.sleep(int(2))   


def CheckDevise(String):
    global counter
    length=len(String)
    print(String[length-2:length])
    if String[length-1:length]=='M':
        counter=0
        greeting[counter]=String[0:1]+'爺爺您好，請您先量測體溫'
        print(greeting[counter])
    elif String[length-1:length]=='F':
        counter=0
        greeting[counter]=String[0:1]+'奶奶您好，請您先量測體溫'
        print(greeting[counter])
    elif String[length-2:length]=='.C':
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
        greeting[counter]='目前收縮壓為'+String[0:int(half)-2]+'mmhg、收縮壓為'+String[int(half)-1:length-4]+'擴張壓,這是您的網頁'
        print(greeting[counter])
    return

while is_looping:
    HealthIndicator ='100kg'#會收到兩種型態的.C or kg #100 100mmhg
    # HealthIndicator=HealthIndicator.decode('utf-8')
    CheckDevise(HealthIndicator)
    robot=threading.Thread(target=voice)
    robot.start()
    robot.join()
    # pusher.send_string("yes")
    print('counter = {} '.format(counter))