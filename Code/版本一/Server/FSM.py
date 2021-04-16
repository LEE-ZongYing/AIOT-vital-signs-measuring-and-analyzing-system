import zmq
import time
import threading
from functools import partial
context = zmq.Context()
recvive = context.socket(zmq.PULL)
recvive.connect("tcp://192.168.0.173:5556")

send_rasp = context.socket(zmq.PUSH)
send_rasp.connect("tcp://192.168.0.173:5555")

sender = context.socket(zmq.PUSH)
sender.connect("tcp://192.168.0.145:5554")

zenbo_recvive = context.socket(zmq.PULL)
zenbo_recvive.connect("tcp://192.168.0.145:5558")

# send_inter = context.socket(zmq.PUSH)
# send_inter.connect("tcp://192.168.0.105:5557")


poller = zmq.Poller()
poller.register(recvive, zmq.POLLIN)

class MeasureEvent(object):
    def __init__(self, ):
        self.card=False
        self.temperature=False
        self.weight=False
        self.pressure=False
        self.state=""
        self.fsm=None
        self.data=""
        self.done=False
        self.offCard=False
    def bind(self,state,fsm):#bind state
        print("bind start")
        self.state=state
        self.fsm=fsm
        print(self.state)
        print(self.fsm)
    def OnlyCard(self):
        self.data = "08" + self.data
        sender.send_string(self.data)
        self.data = ""
        print("onlycard")
    def InitialState(self):
        sender.send_string("00nc")
        #人臉辨識
    #量其他工具
    def CTM(self):
        sender.send_string(str(self.AttributeToNumber())+self.data)
    def CWM(self):
        sender.send_string(str(self.AttributeToNumber())+self.data)
    def CPM(self):
        sender.send_string("0"+str(self.AttributeToNumber())+self.data)
    def CTPM(self):
        sender.send_string(str(self.AttributeToNumber())+self.data)
    def CWPM(self):
        sender.send_string(str(self.AttributeToNumber())+self.data)
    def CTWM(self):
        sender.send_string(str(self.AttributeToNumber())+self.data)
    def OffCard(self):
        self.data = "99" + self.data
        sender.send_string(self.data)
        self.data = ""
        print("offcard")
        time.sleep(10)
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
    def FINISH(self):
        sender.send_string(str(self.AttributeToNumber())+self.data)
class State(object):#全0時初始狀態
    def exec(self,):
        pass
    def exit(self):
        print("test exit success")

class InitialState(State):
    def exec(self,obj1):
        obj1.InitialState()
    def exit(self,obj1):
        print("test exit success")  
class OnlyCard(State):
    def exec(self,obj1):
        obj1.OnlyCard()
    def exit(self,obj1):
        print("test exit success")
class CPM(State):
    def exec(self,obj1):
        obj1.CPM()
    def exit(self,obj1):
        print("test exit success")
class CWM(State):
    def exec(self,obj1):
        obj1.CWM()
    def exit(self,obj1):
        print("test exit success")
class CWPM(State):
    def exec(self,obj1):
        obj1.CWPM()
    def exit(self,obj1):
        print("test exit success")
class CTM(State):
    def exec(self,obj1):
        obj1.CTM()
    def exit(self,obj1):
        print("test exit success")
class CTPM(State):
    def exec(self,obj1):
        obj1.CTPM()
    def exit(self,obj1):
        print("test exit success")
class CTWM(State):
    def exec(self,obj1):
        obj1.CTWM()
    def exit(self,obj1):
        print("test exit success")
class FINISH(State):
    def exec(self,obj1):
        obj1.FINISH()
    def exit(self,obj1):
        print("test exit success")
class OffCard(State):
    def exec(self,obj1):
        obj1.OffCard()
    def exit(self,obj1):
        print("test exit success")

class StateMachine(object):
    def __init__(self):#對應數字:各式狀態
        self.states={0:InitialState(),7:OffCard(),8:OnlyCard(),9:CPM(),10:CWM(),11:CWPM(),12:CTM(),13:CTPM(),14:CTWM(),15:FINISH()}
    def getFsm(self,state):#從此處拿狀態機
        return self.states[state]
    def changeState(self, l, obj1):
            #   如果新產生的訊號和物件原本的執行狀態對應的訊號一致的話
            print('目前狀態為： {}'.format(obj1))
            if l.AttributeToNumber() == obj1:
                #   保持原狀態
                fsm = self.getFsm(obj1)
                fsm.exec(l)
            else:
                #   先退出舊狀態
                print("退出舊狀態")
                old_fsm = self.getFsm(obj1)
                old_fsm.exit(obj1)
                #   執行新狀態
                l.state = l.AttributeToNumber()
                new_fsm = self.getFsm(l.state)
                new_fsm.exec(l)
                if 15 == obj1:
                    return

def run(l,sm):
    #measure=[]
    while True:
        print(l.card)
        data=recvive.recv()
        data = bytes.decode(data)
        print(data)
        length=len(data)
        PreviousState=l.AttributeToNumber()
        if data[length-2:length]=='.C':
            if p.temperature==False:
                p.temperature=True
                p.data=data
        elif data[length-2:length]=='kg':
            if p.weight==False:
                p.weight=True
                p.data=data
        elif data[length-2:length]=='hg':
            if p.pressure==False:
                p.pressure=True
                p.data=data
        elif data=="nc":
            if p.card==True:
                p.card=False
                p.data=data
        if l.AttributeToNumber()==6 or l.AttributeToNumber()==5 or l.AttributeToNumber()==4 or l.AttributeToNumber()==3 or l.AttributeToNumber()==2 or l.AttributeToNumber()==1 or l.AttributeToNumber()==0:
            break
        l.bind(l.AttributeToNumber(),sm.getFsm(l.AttributeToNumber()))
        print(l.card)
        sm.changeState(l,PreviousState)
        if l.AttributeToNumber()==7:
            time.sleep(10)
            break
        
    #measure.append(l)
while True:
    global data,length,data1
    data = "0"
    length = 0
    p=MeasureEvent()
    sm=StateMachine()
    p.bind(p.AttributeToNumber(),sm.getFsm(p.AttributeToNumber()))
    cardstate=p.AttributeToNumber()
    sm.changeState(p,cardstate)
    p.card=False
    p.temperature=False
    p.weight=False
    p.pressure=False
    data1 = zenbo_recvive.recv()
    data1 = data1.decode('utf-8')
    print(data1)
    while True:
        socks = dict(poller.poll(21000))
        if socks:
            if socks.get(recvive) == zmq.POLLIN:
                data=recvive.recv()#少編碼
                data = bytes.decode(data)
                print(data)
                length=len(data)
                print(data[length-2:length-1])
                break
        else:
            break
    if data[length-2:length-1]=='M':
        p.card=True
    elif data[length-1:length]=='F':
        p.card=True
    while p.card==True:#means card input,此時l state = only card other are 0
        p.data=data
        cardstate=p.AttributeToNumber()
        p.bind(p.AttributeToNumber(),sm.getFsm(p.AttributeToNumber()))
        sm.changeState(p,cardstate)
        print(p.card)
        run(p,sm)
        break
    print('完成一趟')