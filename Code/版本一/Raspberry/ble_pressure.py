import pexpect
import time

def Funcpressure():
    mac = "C0:26:DA:01:FF:8E"
    isConnected = False

    device = pexpect.spawn("gatttool -b " + mac  + " -I")
    print("wait connect...")

    while True:
        device.sendline("disconnect")
        device.sendline("connect")

        try:
            device.expect("Connection successful", timeout=3)
            isConnected = True
            print("Connection successful")
        except pexpect.TIMEOUT:
            isConnected = False
            continue

        if not isConnected:
            continue

        try:
            device.sendline("char-write-cmd 0x001f 0200")
            #device.sendline("char-write-cmd 0x000f 0200")
            device.expect("Indication   handle = 0x001e value: ", timeout=5)
            #device.expect("Indication   handle = 0x000e value: ", timeout=5)
        except pexpect.TIMEOUT:
            isConnected = False
            print("Connection failed")
            continue

        device.readline()
        data = device.before
        try:
            pressureS = int(data[3:5], 16) + int(data[6:8], 16)
            pressureD = int(data[9:11], 16)
            #pulse = int(data[42:44], 16)
            return str(pressureS),str(pressureD)
           # print("pulse:" + str(pulse))
        except:
            continue

        isConnected = False
        device.sendline("disconnect")
        time.sleep(10)