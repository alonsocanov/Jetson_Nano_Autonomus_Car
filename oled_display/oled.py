# Basic example of clearing and drawing pixels on a SSD1306 OLED display.
# This example and library is meant to work with Adafruit CircuitPython API.
# Author: Tony DiCola
# License: Public Domain

# Import all board pins.
from board import SCL, SDA
import busio
import time

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess
# Import the SSD1306 module.
import adafruit_ssd1306

import utils


# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)


# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
# Alternatively you can change the I2C address of the device with an addr parameter:
# display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, addr=0x3c)

width = display.width
height = display.height

image = Image.new('1', (width, height))

draw = ImageDraw.Draw(image)

draw.rectangle((0, 0, width, height), outline=0, fill=0)

padding = -2
top = padding
bottom = height-padding

x = 0

# Load default font.
font = ImageFont.load_default()

# Clear the display.  Always call show after changing pixels to make the display
# update visible!
# display.fill(0)

# display.show()

# # Set a pixel in the origin 0,0 position.
# display.pixel(0, 0, 1)
# # Set a pixel in the middle 64, 16 position.
# display.pixel(64, 16, 1)
# # Set a pixel in the opposite 127, 31 position.
# display.pixel(127, 31, 1)
# display.show()
while True:

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "free -m | awk 'NR==2{printf \"Mem:  %.0f%% %s/%s M\", $3*100/$2, $3,$2 }'"
    MemUsage = subprocess.check_output(cmd, shell=True)
    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
    Disk = subprocess.check_output(cmd, shell=True)

    # Print the IP address
    # Two examples here, wired and wireless
    # draw.text((x, top),       "eth0: " +str(utils.get_ip_address('eth0')),  font=font, fill=255)
    draw.text((x, top+8), "wlan0: " +
              str(utils.get_ip_address('wlan0')), font=font, fill=255)

    # Alternate solution: Draw the GPU usage as text
    # draw.text((x, top+8),     "GPU:  " +"{:3.1f}".format(GPU)+" %", font=font, fill=255)
    # We draw the GPU usage as a bar graph
    string_width, string_height = font.getsize("GPU:  ")
    # Figure out the width of the bar
    full_bar_width = width-(x+string_width)-1
    gpu_usage = utils.get_gpu_usage()
    # Avoid divide by zero ...
    if gpu_usage == 0.0:
        gpu_usage = 0.001
    draw_bar_width = int(full_bar_width*(gpu_usage/100))
    draw.text((x, top+8),     "GPU:  ", font=font, fill=255)
    draw.rectangle((x+string_width, top+12, x+string_width +
                    draw_bar_width, top+14), outline=1, fill=1)

    # Show the memory Usage
    draw.text((x, top+16), str(MemUsage.decode('utf-8')), font=font, fill=255)
    # Show the amount of disk being used
    draw.text((x, top+25), str(Disk.decode('utf-8')), font=font, fill=255)

    # Display image.
    # Set the SSD1306 image to the PIL image we have made, then dispaly
    display.image(image)
    display.show()
    # 1.0 = 1 second; The divisor is the desired updates (frames) per second
    time.sleep(1.0)
