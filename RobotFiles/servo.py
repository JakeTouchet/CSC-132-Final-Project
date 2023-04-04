# Fake rpi libary used instead of RPi.GPIO for debugging on
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
bin_pin0 = 19
bin_pin1 = 20
bin_pin2 = 21
bin_pin3 = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(bin_pin0, GPIO.OUT)
GPIO.setup(bin_pin1, GPIO.OUT)
GPIO.setup(bin_pin2, GPIO.OUT)
GPIO.setup(bin_pin3, GPIO.OUT)

def bin_encoder(direction:int, speed:int):
  """Encodes direction and speed values into binary data
  and sends it to the arduino"""

  # Forces direction to be bound to range [0,3]
  direction = min(max(direction,0),3)
  # Forces speed to be bound to range [0,3]
  speed = min(max(speed,0),3)

  # converts int into binary string
  # adds 256 to the number to ensure that
  # the binary conversion is atleast 8 digits long
  # then takes the last three digits as
  # there are currently only 3 bin pins
  dir_bin = bin(direction + 256)[-2:]
  spd_bin = bin(speed + 256)[-2:]
  GPIO.output(bin_pin0, dir_bin[1] == "1")
  GPIO.output(bin_pin1, dir_bin[0] == "1")
  GPIO.output(bin_pin2, spd_bin[1] == "1")
  GPIO.output(bin_pin3, spd_bin[0] == "1")
  print(dir_bin, spd_bin)

def stop() -> None:
  """Tells the servos to stop"""

  bin_encoder(0,0)

def forward(speed:int = 3) -> None:
  """Tells the servos to go forward
   \nspeed:int [0,3]"""
  
  bin_encoder(0,speed)

def backward(speed:int = 3) -> None:
  """Tells the servos to go backward
   \nspeed:int [0,3]"""
  
  bin_encoder(1,speed)

def right(speed:int = 3) -> None:
  """Tells the servos to go right
   \nspeed:int [0,3]"""
  
  bin_encoder(2,speed)

def left(speed:int = 3) -> None:
  """Tells the servos to go left
   \nspeed:int [0,3]"""
  
  bin_encoder(3,speed)

def shutdown() -> None:
  """Runs shutdown sequence"""
  GPIO.cleanup()

def timedTurn(direction:float, x_res=640):
  startTime = time.time()
  timer = abs(direction)/(x_res/2)
  if (direction > 0):
    while (time.time() - startTime < timer):
      right(2)
    stop()
  elif (direction < 0):
    while (time.time() - startTime < timer):
      left(2)
    stop()
  else:
    stop()
