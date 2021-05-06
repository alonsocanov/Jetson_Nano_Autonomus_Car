import unittest
import time

from communication import Communication
from user_input import Keyboard, Joystick


class TestModules(unittest.TestCase):

    # def test_serial_communication(self):
    #     port = '/dev/tty.usbmodem1433401'
    #     baudrate = 9600
    #     timeout = 3
    #     arduino = Communication(port)
    #     for i in range(10):
    #         data = user_input()
    #         arduino.send(data)
    #         while not arduino.buffer:
    #             arduino.receive()
    #             if arduino.buffer:
    #                 print(arduino.buffer)
    #         arduino.set_buffer(None)

    # def test_key_input(self):
    #     initInpuWindow()
    #     key_q = False
    #     while not key_q:
    #         key_q = get_key('q')
    #         if get_key('LEFT'):
    #             print('LEFT')

    #         if get_key('RIGHT'):
    #             print('RIGHT')
    #         if get_key('UP'):
    #             print('UP')
    #         if get_key('DOWN'):
    #             print('DOWN')

    # def test_motor_control_input(self):
    #     port = '/dev/tty.usbmodem1433401'
    #     baudrate = 9600
    #     timeout = 3
    #     arduino = Communication(port, baudrate, timeout)
    #     keyboard = Keyboard()
    #     key_q = False
    #     t = time.time()
    #     while not key_q:
    #         key_q = keyboard.key_q()
    #         data = keyboard.arrow_control()

    #         if data:
    #             t = time.time()
    #             arduino.send(data)
    #         if time.time() - t > 20:
    #             key_q = True

    #         while not arduino.buffer and data:
    #             arduino.receive()
    #             if arduino.buffer:
    #                 print(arduino.buffer)
    #         arduino.set_buffer(None)

    def test_motor_control_joysick(self):
        port = '/dev/tty.usbmodem1433401'
        baudrate = 9600
        timeout = 3
        arduino = Communication(port, baudrate, timeout)
        joystick = Joystick()
        key_q = False
        t = time.time()
        while not key_q:
            key_q = joystick.getJS('R2')
            data_1 = joystick.getJS('axis2') * 45
            data_2 = joystick.getJS('axis1')
            data_3 = '100'
            data = ','.join([str(data_1), str(data_2), data_3])

            if data:
                t = time.time()
                arduino.send(data)
            if time.time() - t > 20:
                key_q = True

            while not arduino.buffer and data:
                arduino.receive()
                if arduino.buffer:
                    print(arduino.buffer)
            arduino.set_buffer(None)


if __name__ == '__main__':
    unittest.main()
