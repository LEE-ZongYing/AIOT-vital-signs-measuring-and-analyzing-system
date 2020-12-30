import pexpect
import time

mac = " C0:26:DA:0C:0E:E2"
isConnected = False

device = pexpect.spawn("gatttool -b " + mac  + " -I")
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
        device.sendline("char-read-cmd 0x001f 0200")
        device.expect("Indication  handle = 0x000e value: ",timeout=5)
    except pexpect.TIMEOUT:
        isConnected = False
        continue

    device.readline()
    data = device.before
    value = data[6:8] + data[3:5]
    try:
        temperature = int(value, 16)
        print("temperature:" + str(temperature / 100.0))
    except:
        continue

    isConnected = False
    device.sendline("disconnect")
    time.sleep(100)