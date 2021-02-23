import zmq
import time
from functools import partial
context = zmq.Context()
recvive = context.socket(zmq.PULL)
recvive.connect("tcp://192.168.0.106:5554")

sender = context.socket(zmq.PUSH)
sender.connect("tcp://192.168.0.106:5556")
#送資料格式(ATN,葉韋均均君,MM/FF）
counter = 100
class MeasureEvent(object):
    def __init__(self, ):
        self.card=False
        self.temperature=False
        self.weight=False
        self.pressure=False
        self.state=""
        self.fsm=None
    def bind(self,state,fsm):#bind state
        self.state=state
        self.fsm=fsm
    def OnlyCard(self):
        #zenbo say 你好....先生/小姊，健保卡資料以讀取，請前往量測生理指標
        #send(self.AttributeToNumber,)
        
    def InitialState(self):
        #人臉辨識
        #send
    def CPM(self):
        #send
    def CTM(self):
        print('other')
    def EndState(self):#全部量測+卡完成
        #Call PI存資料
    def AttributeToNumber(self):
        number=0
        if self.card==True:
            number+=8
            if self.temperature==True:
                number+=4
                if self.weight==True:
                    number+=2
                    if self.pressure==True:
                        number+=1
        return number

class State(object):#全0時初始狀態
    def exec(self,):
        obj1.InitialState()#寫告訴機器人做什麼事情
    def exit(self):
        pass
class OnlyCard(object):
    def exec(self,):
        obj1.InitialState(self)
    def exit(self):
        pass
class CPM(state):
    def exec(self,):
        obj1.CPM()
    def exit(self):
        pass
class CWM(object):
    def exec(self,):
        obj1.CWM()
    def exit(self):
        pass
class CTM(object):
    def exec(self,):
        obj1.CTM()
    def exit(self):
        pass
# 2type and finish
    
class StateMachine(object):
    def __init__(self):#對應數字:各式狀態
        self.states={0:InitialState(),8:OnlyCard(),9:CPM(),10:CWM(),11:CWPM(),12:CTM(),13:CTPM(),14:CTWM(),15:FINISH()}
    def getFsm(self,state):#從此處拿狀態機
        return self.states[state]
    def changeState(self, NewState, obj1):
            #   如果新產生的訊號和物件原本的執行狀態對應的訊號一致的話
            print('目前狀態為： {}'.format(obj1.state))
            if NewState == obj1.state:
                #   保持原狀態
                fsm = self.getFsm(obj1.state)
                fsm.exec(obj1)
            else:
                #   先退出舊狀態
                old_fsm = self.getFsm(obj1.state)
                old_fsm.exit(obj1)
                #   執行新狀態
                obj1.state = NewState
                new_fsm = self.getFsm(NewState)
                new_fsm.exec(obj1)
                if 15 == obj1.state:
                    return
                
                
def run(l,sm):
    #measure=[]
    while
        data=context.recv()
        l=CheckDevice(data,l)#send data and know who they were
        l.bind(l.AttributeToNumber,sm.getFsm(l.AttributeToNumber))
        sm.changeState(l.AttributeToNumber,l)
        if l.AttributeToNumber==15:
            break
    return
        
        
    #measure.append(l)

while True:
    data=context.recv()#少編碼
    l=CheckCard(data)
    sm=StateMachine()
    while l.card==False:
        #00~07的狀態
        #send signal to zenbo for face recognization
        #收到yes ＝ break
        break
    while l.card==True:#means card input,此時l state = only card other are 0
        l.bind(l.AttributeToNumber,sm.getFsm(l.AttributeToNumber))
        sm.changeState(l.AttributeToNumber,l)
        run(l,sm)
        break
    print('完成一趟')

def CheckDevice(String,l):
    global counter
    length=len(String)
    print(String[length-1:length])
    if String[length-2:length]=='.C':
        counter=1
        greeting[counter]='目前體溫為'+String[0:length-2]+'度,請前往量測體重'
        print(greeting[counter])
        if l.temperature==False:
            l.temperature=True
        return l
    elif String[length-2:length]=='kg':
        counter=2
        greeting[counter]='目前體重為'+String[0:length-2]+'公斤,請前往量測血壓以及血糖'
        print(greeting[counter])
        if l.weight==False:
            l.weight=True
        return l
    elif String[length-4:length]=='mmhg':
        counter=3
        half=len(String)/2
        greeting[counter]='目前收縮壓為'+String[0:int(half)-2]+'mmhg、收縮壓為'+String[int(half)-1:length-4]+'擴張壓,這是您的網頁'
        print(greeting[counter])
        if l.pressure==False:
            l.pressure=True
        return l
    #elif 拔卡
        #obj1.card=False


def CheckCard(String):
    global counter
    length=len(String)
    print(String[length-1:length])
    if String[length-1:length]=='M':
        # counter=0
        # greeting[counter]=String[0:1]+'爺爺您好，請您先量測體溫'
        # print(greeting[counter])
        obj1=MeasureEvent()
        obj1.card=True
        return obj1
    elif String[length-1:length]=='F':
        counter=0
        greeting[counter]=String[0:1]+'奶奶您好，請您先量測體溫'
        print(greeting[counter])
        obj1=MeasureEvent()#為一種狀態
        obj1.card=True
        return obj1
    else:
        obj1=MeasureEvent()#為一種狀態
        obj1.card=False
        return obj1
        #Zenbo會說請先插入健保卡在量測喔，不然我不知道你是誰^^
        #return 
