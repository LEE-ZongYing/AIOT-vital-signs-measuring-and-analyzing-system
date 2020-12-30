import time
import zmq
from cardreader_RPi1 import card
from ble_weight import Funcweight
from ble_fora40 import Functemperature
from ble_pressure import Funcpressure
from smartcard.CardRequest import CardRequest
import pymysql

context = zmq.Context()
revive = context.socket(zmq.PULL)
revive.bind("tcp://192.168.0.12:5555")
socket = context.socket(zmq.PUSH)
socket.bind("tcp://192.168.0.12:5554")           #socket

poller = zmq.Poller()
poller.register(revive, zmq.POLLIN)

while True:
    db=pymysql.connect("192.168.0.13","root","123456","cardreader") #mysql
    cursor=db.cursor()

    response = revive.recv()
    print(response)
    print('請插入健保卡')
    cardrequest = CardRequest(timeout=10000)    
    cardservice = cardrequest.waitforcard()
    cardnumber,name_big5,idnumber,birthday,psex,carddate = card()
    person = name_big5 + psex
    socket.send_string(person)
    time.sleep(1)
    pollertime = dict(poller.poll(100000))
    if pollertime:
        if pollertime.get(revive) == zmq.POLLIN:
           response = revive.recv()
           print(response)
        else:
            print("continue")
    time.sleep(3)
    
    
    def main():
        temperature = Functemperature()      #temperature
        temperature_add = temperature + ".C"
        print(temperature_add)
        socket.send_string(temperature_add)
        time.sleep(1)
        pollertime = dict(poller.poll(100000))
        if pollertime:
            if pollertime.get(revive) == zmq.POLLIN:
               response = revive.recv()
               print(response)
            else:
                print("continue")    
        time.sleep(3)

        weight = Funcweight()                #weight
        weight_add = weight + "kg"
        print(weight_add)
        socket.send_string(weight_add)
        time.sleep(1)
        pollertime = dict(poller.poll(100000))
        if pollertime:
            if pollertime.get(revive) == zmq.POLLIN:
               response = revive.recv()
               print(response)
            else:
                print("continue")
        time.sleep(3)
        
        pressureS,pressureD = Funcpressure()  #pressure
        pressureD_add = pressureD +"mmhg"
        print(pressureS + " " +pressureD_add)
        Strpressure = pressureS + " "+ pressureD_add
        socket.send_string(Strpressure)
        time.sleep(1)
        pollertime = dict(poller.poll(100000))
        if pollertime:
            if pollertime.get(revive) == zmq.POLLIN:
               response = revive.recv()
               print(response)
            else:
                print("continue")
        time.sleep(3)
        socket.send_string("AllDone")
        time.sleep(2)
        pollertime = dict(poller.poll(100000))
        if pollertime:
            if pollertime.get(revive) == zmq.POLLIN:
                response = revive.recv()
                print(response)
            else:
                print("continue")
        
        sql="INSERT INTO iccard(name,id_card,cardnum,birthday,sex,carddate,temperature,weight,pressureS,pressureD)VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (name_big5,idnumber,cardnumber,birthday,psex,carddate,temperature,weight,pressureS,pressureD)
        try:
            cursor.execute(sql);
            db.commit();
        except:
            print('error');

        db.close()
            
    main()
    
    
   
    
    print('請取回健保卡')
        
    while True:
        cards = cardrequest.waitforcardevent()
        if 0 == len(cards):
            break
        time.sleep(.3)
    
    
