# Fake rpi library used instead of RPi.GPIO for debugging on
# a system other then the raspberry pi

import io
import os

def is_raspberrypi():
  """Returns true if running on a raspberry pi"""
  try:
      with io.open('/sys/firmware/devicetree/base/model', 'r') as m:
          if 'raspberry pi' in m.read().lower(): return True
  except Exception: pass
  return False

# Use real gpio on rpi
# Use fake gpio on anything else
if is_raspberrypi():
  import RPi.GPIO as GPIO
else:
  import fake_rpi
  GPIO = fake_rpi.fake_rpi.RPi.GPIO

import time

# Sets up output pins for communication with arduino
triggerPin = 15
dataPin = 14

GPIO.setmode(GPIO.BCM)
GPIO.setup(triggerPin, GPIO.OUT)
GPIO.setup(dataPin, GPIO.OUT)

def transmit():
   data = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

   GPIO.output(triggerPin, GPIO.HIGH)

if __name__ == "__main__":
   transmit()