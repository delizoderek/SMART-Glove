import bluetooth
import sys
import serial

def bluez():
    count = 0
    port = 1

    nearby_devices = bluetooth.discover_devices() 
    for bdaddr in nearby_devices:
        count += 1
        print count, ". ", bluetooth.lookup_name( bdaddr )  

    selection = input("> ") - 1
    print "You have selected", bluetooth.lookup_name(nearby_devices[selection])
    bd_addr = nearby_devices[selection]

    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((bd_addr,port))
    sock.send("Hello!")
    sock.close()

ser = serial.Serial("COM11",9600)
print "Connected"
ser.write("Ready for data")
print "Sent Connection Call"
cats = []
for i in range(0,5):
    cats.append(ser.read(1))

print ''.join(cats)
