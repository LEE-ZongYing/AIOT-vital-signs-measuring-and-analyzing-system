import zmq
import time
from functools import partial
context = zmq.Context()
recvive = context.socket(zmq.PULL)
recvive.connect("tcp://192.168.0.12:5554")

sender = context.socket(zmq.PUSH)
sender.connect("tcp://192.168.0.3:5556")

puller = context.socket(zmq.PULL)
puller.connect("tcp://192.168.0.3:5557")

pusher = context.socket(zmq.PUSH)
pusher.connect("tcp://192.168.0.12:5555")

poller = zmq.Poller()
poller.register(puller, zmq.POLLIN)


while True:
    print("waittings")
    data1 = puller.recv()
    data2 = bytes.decode(data1)
    pusher.send_string(data2)
    print("正在轉發")
    i=5
    while i>0:
        i-=1
        data = recvive.recv()
        sdata = data.decode('utf-8')
        print(sdata)
        print("正在轉發")
        sender.send_string(sdata)
        print("waittings")
        pullertime = dict(poller.poll(100000))
        if pullertime:
            if pullertime.get(puller) == zmq.POLLIN:
                basp = puller.recv()
                print(basp)
                basp1 = bytes.decode(basp)
                pusher.send_string(basp1)
                print("正在轉發")
        else:
            print("error: message timeout")