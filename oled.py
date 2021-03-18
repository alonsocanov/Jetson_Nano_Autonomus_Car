# -*- coding: utf-8 -*-

'''
The MakerFocus I2C OLED Display is meant to be comptible with Adafruit CircuitPython API.
The objective of this stript is to display the Jetson Nano's information such as its IP address.
It can also display the GPU usage, CPU usage and memory usage, by default it is deactivated due
beena a request loop

'''


# Import all board pins.
from board import SCL, SDA
import busio
import time
# Pillow library for image manipulation
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess
# Import the SSD1306 module.
import adafruit_ssd1306
# library for needed functions
from oled_display.utils import get_ip_address, get_gpu_usage

DIPLAY_IP = True

# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)
# OLED pixels
WIDTH = 128
HEIGHT = 32

# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
display = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)
# Alternatively you can change the I2C address of the device with an addr parameter:
# display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, addr=0x3c)

# Create a sigle bit image of size (WIDTH, HEIGHT)
image = Image.new('1', (WIDTH, HEIGHT))
# Create a draw object to manipulate image
draw = ImageDraw.Draw(image)
# Draw a black filled box to clear the image
draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)

# Define a padding
padding = -2
# Top and lower padding
top = padding
bottom = HEIGHT-padding

x = 1

# Load default font to write on image
font = ImageFont.load_default()


if DIPLAY_IP:
    # Print the IP address
    # Two examples here, wired and wireless
    eth_address = str(get_ip_address('eth0'))
    if eth_address != 'None':
        draw.text((x, top), "eth0: " + eth_address,  font=font, fill=255)
        top += 8
    wlan_address = str(get_ip_address('wlan0'))
    if wlan_address != 'None':
        draw.text((x, top), "wlan0: " + wlan_address, font=font, fill=255)
        top += 8
    # Display image.
    # Set the SSD1306 image to the PIL image we have made
    display.image(image)
    # Display image in screen
    display.show()
else:

    while True:

        # Draw a black filled box to clear the image
        draw.rectangle((0, 0, width, height), outline=0, fill=0)

        # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
        cmd = "free -m | awk 'NR==2{printf \"Mem:  %.0f%% %s/%s M\", $3*100/$2, $3,$2 }'"
        MemUsage = subprocess.check_output(cmd, shell=True)
        cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
        Disk = subprocess.check_output(cmd, shell=True)

        # Print the IP address
        # Two examples here, wired and wireless
        # draw.text((x, top), "eth0: " +str(get_ip_address('eth0')),  font=font, fill=255)
        draw.text((x, top+8), "wlan0: " +
                  str(get_ip_address('wlan0')), font=font, fill=255)

        # Alternate solution: Draw the GPU usage as text
        # draw.text((x, top+8),     "GPU:  " +"{:3.1f}".format(GPU)+" %", font=font, fill=255)
        # We draw the GPU usage as a bar graph
        string_width, string_height = font.getsize("GPU:  ")
        # Figure out the width of the bar
        full_bar_width = WIDTH-(x+string_width)-1
        gpu_usage = get_gpu_usage()
        # Avoid divide by zero ...
        if gpu_usage == 0.0:
            gpu_usage = 0.001
        draw_bar_width = int(full_bar_width*(gpu_usage/100))
        draw.text((x, top+8),     "GPU:  ", font=font, fill=255)
        draw.rectangle((x+string_width, top+12, x+string_width +
                        draw_bar_width, top+14), outline=1, fill=1)

        # Show the memory Usage
        draw.text((x, top+16), str(MemUsage.decode('utf-8')),
                  font=font, fill=255)
        # Show the amount of disk being used
        draw.text((x, top+25), str(Disk.decode('utf-8')), font=font, fill=255)

        # Display image.
        # Set the SSD1306 image to the PIL image we have made
        display.image(image)
        # Display image in screen
        display.show()
        # 1.0 = 1 second; The divisor is the desired updates (frames) per second
        time.sleep(1.0)
