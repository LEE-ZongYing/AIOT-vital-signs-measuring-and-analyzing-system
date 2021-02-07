import zmq
import time
from functools import partial
context = zmq.Context()
recvive = context.socket(zmq.PULL)
recvive.connect("tcp://192.168.0.103:5554")

send_rasp = context.socket(zmq.PUSH)
recvive.connect("tcp://192.168.0.103:5555")

sender = context.socket(zmq.PUSH)
sender.connect("tcp://192.168.0.103:5556")



counter = 100
class MeasureEvent(object):
    def __init__(self, ):
        self.card=False
        self.temperature=False
        self.weight=False
        self.pressure=False
        self.number=0
        self.state=""
        self.fsm=None
    def bind(self,state,fsm):#bind state
        self.state=state
        self.fsm=fsm
    def OnlyCard(self):
        #zenbo say 你好....先生/小姊，健保卡資料以讀取，請前往量測生理指標
        sender.send_string(data)
    def InitialState(self):
        pass
        #人臉辨識
    def CPM(self):
        sender.send_string(data)
    #量其他工具
    def CTM(self):
        print('other')
    def FINISH(self):#全部量測+卡完成
        #Call PI存資料
        print("完成")
class State(object):#全0時初始狀態
    def NoticeRobot(self,):
        pass
    def exit(self):
        print("test exit success")

class InitialState(State):
    def NoticeRobot(self,obj1):
        obj1.InitialState()
    def exit(self):
        print("test exit success")  
class OnlyCard(State):
    def NoticeRobot(self,obj1):
        obj1.OnlyCard()
    def exit(self):
        print("test exit success")
class CPM(State):
    def NoticeRobot(self,obj1):
        obj1.CPM()
    def exit(self):
        print("test exit success")
class CWM(State):
    def NoticeRobot(self,obj1):
        obj1.CWM()
    def exit(self):
        print("test exit success")
class CWPM(State):
    def NoticeRobot(self,obj1):
        obj1.CWPM()
    def exit(self):
        print("test exit success")
class CTM(State):
    def NoticeRobot(self,obj1):
        obj1.CTM()
    # @property
    # def s(self, )
    
    # def get_value(self,)

    # def send(self, unit):
    #     pass

class CTPM(State):
    def NoticeRobot(self,obj1):
        obj1.CTPM()
    def exit(self):
        print("test exit success")
class CTWM(State):
    def NoticeRobot(self,obj1):
        obj1.CTWM()
    def exit(self):
        print("test exit success")
class FINISH(State):
    def NoticeRobot(self,obj1):
        obj1.FINISH()
    def exit(self):
        print("test exit success")

class StateMachine(object):
    def __init__(self):
        self.states = {0: InitialState(),8: OnlyCard(),9: CPM(),10: CWM(),11: CWPM(),12: CTM(),13: CTPM(),14: CTWM(),15: FINISH()}
    def getFsm(self, state):
        return self.states[state]
    def changeState(self, NewState, objs):
        for obj1 in objs:
    #   如果新產生的訊號和物件原本的執行狀態對應的訊號一致的話
            if NewState == obj1.state:
            #   保持原狀態
                fsm = self.getFsm(obj1.state)
                fsm.NoticeRobot(obj1)
            else:
            #   先退出舊狀態
                old_fsm = self.getFsm(obj1.state)
                old_fsm.exit(obj1)
            #   執行新狀態
                obj1.state = NewState
                new_fsm = self.getFsm(NewState)
                new_fsm.NoticeRobot(obj1)      

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
        obj1=MeasureEvent()#為一種狀態
        obj1.card=True
        return obj1
    else:
        pass
        #Zenbo會說請先插入健保卡在量測喔，不然我不知道你是誰^^
        #return 
        #send signal to zenbo 
def CheckDevice(String,l):
    global counter
    length=len(String)
    print(String[length-1:length])
    if String[length-2:length]=='.C':
        counter=1
        if l.temperature==False:
            l.temperature=True
        return l
    elif String[length-2:length]=='kg':
        counter=2
        if l.weight==False:
            l.weight=True
        return l
    elif String[length-4:length]=='mmhg':
        counter=3
        if l.pressure==False:
            l.pressure=True
        return l
    #elif 拔卡
        #obj1.card=False
def run(l):
    while True:
        print("going")
        sm=StateMachine()
        measure=[]
        l=CheckDevice(data,l)
        ATN=MeasureEvent()
        ATN.number=0
        if ATN.card==True:
            ATN.number = 8
            if ATN.temperature==True:
                ATN.number+=4
                if ATN.weight==True:
                    ATN.number+=2
                    if ATN.pressure==True:
                        ATN.number+=1
        ATN.bind(ATN.number,sm.getFsm(ATN.number))
        measure.append(l)
        sm.changeState(ATN.number,measure)
while True:
    data=recvive.recv()#少編碼
    data = bytes.decode(data)
    l=CheckCard(data)
    while l.card==True:#means card input,此時l state = only card other are 0 
        run(1)
        break