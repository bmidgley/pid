# pid

# sda to 4
# scl to 6
# vcc to 8
# gnd to 10
# gy-521's vcc to pin 1

# sudo apt install python-pip
# sudo pip install RPi.GPIO Adafruit-SSD1306 mpu6050-raspberrypi
# add to /etc/rc.local before exit: (python /home/pi/pid/pid.py) &

import RPi.GPIO as GPIO
from mpu6050 import mpu6050
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.output(4, GPIO.HIGH)
GPIO.output(23, GPIO.LOW)

# Raspberry Pi pin configuration:
RST = 24

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Create blank image for drawing.

disp.begin()
disp.clear()
disp.display()

width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)

# accel

sensor = mpu6050(0x68)

x0 = 64
y0 = 32

snake = []

length = 8

while True:
  draw.rectangle((0, 0, width - 1, height - 1), outline=255, fill=0)

  a = sensor.get_accel_data()
  x1 = x0 + a['y']
  y1 = y0 - a['x']
  snake.append((x1, y1))

  x0, y0 = snake[0]
  for (x,y) in snake:
    x = x % width
    y = y % height
    if (abs(x - x0) + abs(y - y0) < 20):
      draw.line((x0, y0, x, y), fill=255)
    x0 = x
    y0 = y

  disp.image(image)
  disp.display()

  if(len(snake) > length):
    snake.pop(0)

  GPIO.output(23, GPIO.HIGH if (x0 < 5 or y0 < 5) else GPIO.LOW)

