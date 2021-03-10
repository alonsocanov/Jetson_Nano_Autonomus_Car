import serial
import sys
from serial import SerialException
#  Install using pip3 install pyserial


def main():
    serial_comm = serial.Serial()

    # Configure the baud rate and it should be equal to the Arduino code serial communication baud rate
    serial_comm.baudrate = 9600

    # Configure the COM port as needed '/dev/ttyXXXX' is applicable for Linux systems
    serial_comm.port = '/dev/ttyACM0'

    # Configure timeout seconds
    serial_comm.timeout = 10

    try:
        serial_comm.open()
    except serial.SerialException:
        # Print an error when the serial communication isn't available
        print("Could not open port")

    while (True):
        if serial_comm.isOpen():
            print("Serial Incoming Data: {}".format(serial_comm.readline()))
        else:
            print("Exiting")
            break
    sys.exit()


if __name__ == "__main__":
    main()
