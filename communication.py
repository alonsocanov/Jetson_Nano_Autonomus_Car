import serial
import time
import sys


class Communication:
    def __init__(self, port, baudrate=9600, timeout=.1):
        try:
            self.__ser = serial.Serial(port=port,
                                       baudrate=baudrate, timeout=timeout)
        except serial.serialutil.SerialException as error:
            print('Port non existant:', port)
            print(error)
            sys.exit(1)
        # self.__ser.write(str.encode('Connexion with arduino \n'))
        self.__buff = None
        time.sleep(2)

    def send(self, data):
        if not isinstance(data, str):
            data = str(data)
        rtxt = ''.join([data, '\n'])
        self.__ser.write(str.encode(rtxt))
        print("Message sent")

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

    def set_buffer(self, val):
        self.__buff = val
