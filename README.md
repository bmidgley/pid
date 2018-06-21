# pid pi (zero) game platform

Requires an i2c ssd1306 display and a gy-521 accelerometer. Buzzer attaches to gnd and bcm23.

sudo raspi-config # Advanced/I2C/Yes
sudo apt install python-pip
sudo pip install RPi.GPIO Adafruit-SSD1306 mpu6050-raspberrypi
sudo vi /etc/rc.local # add before exit:
  (python /home/pi/pid/pid.py) &
