from time import sleep
import serial
import sys
import threading
# these codes are for bluetooth
# hint: please check the function "sleep". how does it work?

class bluetooth:
    def __init__(self, port: str):
        self.ser = serial.Serial(port, 9600)

    def is_open(self) -> bool:
        return self.ser.is_open

    def waiting(self) -> bool:
        return self.ser.in_waiting

    def do_connect(self,port):
        self.disconnect()
        print("Connecting...")
        try:
            self.ser = serial.Serial(port,9600,timeout=2)
            print("connect success")
            print("")
        except serial.serialutil.SerialException:
            print("fail to connect")
            print("")
            return False
        return True


    def disconnect(self):
        self.ser.close()

    def SerialWrite(self,output):
        # send = 's'.encode("utf-8")
        send = output.encode("utf-8")
        self.ser.write(send)

    def SerialReadString(self):
        # TODO: Get the information from Bluetooth. Notice that the return type should be transformed into hex.
        waiting = self.waiting()
        if waiting:
            receiveMsg = self.ser.readline().decode("utf-8")[:-1]
            return receiveMsg
        return ""

    def SerialReadByte(self):
        sleep(0.05)
        waiting = self.ser.inWaiting()
        rv = self.ser.read(waiting)
        if(rv):
            UID = hex(int.from_bytes(rv, byteorder='big', signed=False))
            self.ser.flushInput()
            return UID
        else:
            return 0
def read():
    while True:
        if bt.waiting():
            print(bt.SerialReadString())

def write():
    while True:
        msgWrite = input()
        
        if msgWrite == "exit": sys.exit()
    
        bt.SerialWrite(msgWrite + "\n")

if __name__ == "__main__":
    # Please modify the port name.
    bt = bluetooth("/dev/tty.038-SerialPort") 
    while not bt.is_open(): pass
    print("BT Connected!")

    readThread = threading.Thread(target=read)
    readThread.daemon = True
    readThread.start()

    # read()
    while True:
        msgWrite = input()
        
        if msgWrite == "exit": sys.exit()
    
        bt.SerialWrite(msgWrite + "\n")
