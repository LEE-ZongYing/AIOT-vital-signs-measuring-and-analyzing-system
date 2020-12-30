# -*- coding: utf-8 -*-

from smartcard.System import readers

def card():

    SelectAPDU = [ 0x00, 0xA4, 0x04, 0x00, 0x10, 0xD1, 0x58, 0x00, 0x00, 0x01, 0x00,
               0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x11, 0x00 ]

    ReadProfileAPDU = [ 0x00, 0xca, 0x11, 0x00, 0x02, 0x00, 0x00 ]

    r = readers()
    print("Available readers:", r)

    reader = r[0]
    print ("Using:", reader)

    connection = reader.createConnection()
    connection.connect()

    data, sw1, sw2 = connection.transmit(SelectAPDU)
    print ("Select Applet: %02X %02X" ,sw1, sw2)

    data, sw1, sw2 = connection.transmit(ReadProfileAPDU)

    print ("Command: %02X %02X" ,sw1, sw2)
    cardnumber="".join(chr(i) for i in data[0:12])
    name = "".join(chr(i) for i in data[12:18])
    name_big5 = name.encode('ISO-8859-1').decode('big5')
    idnumber="".join(chr(i) for i in data[32:42])
    birthday="".join(chr(i) for i in data[43:49])
    psex="".join(chr(i) for i in data[49:50])
    carddate="".join(chr(i) for i in data[51:57])
    print ('Card Number : ' , cardnumber)
    print ('Name :' '',name_big5)
    print ('ID Nu-mber : ' , idnumber)
    print ('Birthday : ' , birthday)
    print ('Sex : ' ,psex )
    print ('Card Date : ' , carddate)
    return cardnumber,name_big5,idnumber,birthday,psex,carddate

    
