# pid

# sda to 4
# scl to 6
# vcc to 8
# gnd to 10
# gy-521's vcc to pin 1

# sudo apt install python-pip
# sudo pip install RPi.GPIO Adafruit-SSD1306 mpu6050-raspberrypi
# add to /etc/rc.local before exit: (python /home/pi/pid/pid.py) &

import time

import RPi.GPIO as GPIO
from mpu6050 import mpu6050
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)
GPIO.output(4, GPIO.HIGH)

# Raspberry Pi pin configuration:
RST = 24

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Load default font.
font = ImageFont.load_default()
#draw.text((x, top),    'Hello',  font=font, fill=255)
#draw.text((x, top+20), 'World!', font=font, fill=255)

sensor = mpu6050(0x68)

x0 = 0
y0 = 0
x1 = 0
y1 = 0

while True:
  a = sensor.get_accel_data()
  x1 = (x1 + a['y'])
  y1 = (y1 - a['x'])
  if (x1 == x1 % width and y1 == y1 % height):
    draw.line((x0, y0, x1, y1), fill=255)
  x1 = x0 = x1 % width
  y1 = y0 = y1 % height

  disp.image(image)
  disp.display()

