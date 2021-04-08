import serial
import time


ser = serial.Serial(port='/dev/tty.usbmodem1433401',
                    baudrate=115200, timeout=3)


counter = 32  # Below 32 everything in ASCII is gibberish
while True:
    counter += 1
    # Convert the decimal number to ASCII then send it to the Arduino
    ser.write(bytes(str(counter), 'utf-8'))
    print(counter)
    # Read the newest output from the Arduino
    print(ser.readline().decode('utf-8'))
    time.sleep(.1)  # Delay for one tenth of a second
    if counter == 255:
        counter = 32
