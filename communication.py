import serial
import time


class Communication:
    def __init__(self, port, baudrate=9600, timeout=.1):
        self.__ser = serial.Serial(port=port,
                                   baudrate=baudrate, timeout=timeout)
        # self.__ser.write(str.encode('Connexion with arduino \n'))
        self.__buff = None
        time.sleep(2)

    def send(self, data):
        if not isinstance(data, str):
            data = str(data)
        rtxt = ''.join([data, '\n'])
        self.__ser.write(str.encode(rtxt))
        print("jetson: Message sent")

    def receive(self):
        if self.__ser.inWaiting() > 0:
            recep = self.__ser.readline()[:-2]
            try:
                self.__buff = str(recep, 'utf-8')
            except UnicodeDecodeError:
                self.__buff = None

        else:
            self.__buff = None
        return self.__buff

    @property
    def buffer(self):
        return self.__buff


def main():
    port = '/dev/tty.usbmodem1433401'
    baudrate = 9600
    timeout = 3
    arduino = Communication(port)
    data = "10,20,30,40"
    idx = 0
    arduino.send(data)
    while not arduino.buffer:
        arduino.receive()
        if arduino.buffer:
            print(arduino.buffer)

        # # Convert the decimal number to ASCII then send it to the Arduino
        # ser.write(str.encode(data))
        # # Delay for one tenth of a second
        # time.sleep(.1)
        idx += 1
        # if idx == 100:
        #     arduino.send_data(data)
        #     time.sleep(.5)
        #     arduino.receive_data()
        #     # print(arduino.buffer)
        #     time.sleep(.5)


    # Read the newest output from the Arduino
    # print(ser.readline().decode('utf-8'))
main()
