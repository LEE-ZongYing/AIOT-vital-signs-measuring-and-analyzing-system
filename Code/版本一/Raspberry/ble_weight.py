import pexpect
import time
def Funcweight():
    mac = "C0:26:DF:00:8A:CB"
    isConnected = False
    device = pexpect.spawn("gatttool -b " + mac  + " -t random -I")
    print("wait connect...")

    while True:
        device.sendline("disconnect")
        device.sendline("connect")

        try:
            device.expect("Connection successful", timeout=3)
            isConnected = True
        except pexpect.TIMEOUT:
            isConnected = False
            continue

        if not isConnected:
            continue

        try:
            device.sendline("char-write-cmd 0x001c 0100")
            device.expect("Notification handle = 0x001b value: 01 00", timeout=5)
            device.sendline("char-write-cmd 0x001b 5171020000a367")
            device.expect("Notification handle = 0x001b value: 00 00 00 00 00 00 00 00", timeout=5)
        except pexpect.TIMEOUT:
            isConnected = False
            continue

        data = device.before
        value = data[357:359] + data[360:362]
        try:
            weight = int(value, 16)
            return str(weight / 10.0)
            break
        except:
            continue
        isConnected = False
        device.sendline("disconnect")
        time.sleep(10)