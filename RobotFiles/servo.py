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
triggerPin = 4
dataPin0 = 17
dataPin1 = 18
dataPin2 = 22
dataPin3 = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(triggerPin, GPIO.OUT)
GPIO.setup(dataPin0, GPIO.OUT)
GPIO.setup(dataPin1, GPIO.OUT)
GPIO.setup(dataPin2, GPIO.OUT)
GPIO.setup(dataPin3, GPIO.OUT)

def transmit(direction = 0, speed = 0, timer = 0, pulseWidth: float = 12/1000):

  direction_bin = bin(direction + 1024)[-3:]
  speed_bin = bin(speed + 1024)[-5:]
  timer_bin = bin(timer + 1024)[-8:]

  #print(timer_bin,speed_bin,direction_bin)

  data = [int(i) for i in str(direction_bin)[::-1]] + [int(i) for i in str(speed_bin)[::-1]] + [int(i) for i in str(timer_bin)[::-1]]
  dataSplit = []
  for i in range(0, len(data)//4):
    dataSplit.append([\
      data[0 + 4*i],
      data[1 + 4*i],
      data[2 + 4*i],
      data[3 + 4*i]])

  print(dataSplit)
  GPIO.output(triggerPin, GPIO.HIGH)
  time.sleep(pulseWidth/2)
  GPIO.output(triggerPin, GPIO.LOW)
  for halfByte in dataSplit:
    GPIO.output(dataPin0, halfByte[0])
    GPIO.output(dataPin1, halfByte[1])
    GPIO.output(dataPin2, halfByte[2])
    GPIO.output(dataPin3, halfByte[3])
    time.sleep(pulseWidth)
  GPIO.output(dataPin0, GPIO.LOW)

def stop() -> None:
  """Tells the servos to stop"""

  transmit(direction=0, speed=0, timer=0)

def forward(velocity:int = 3, time:float = 0) -> None:
  """Tells the servos to go forward
   \nspeed:int [0,3]
   \ntimer:float [0, 2.55] (seconds)"""
  _timer = min(max(int(time*100),0),255)
  transmit(direction=0, speed=int(31 * (velocity/3)), timer=_timer)

def backward(velocity:int = 3, time:float = 0) -> None:
  """Tells the servos to go backward
   \nspeed:int [0,3]
   \ntimer:float [0, 2.55] (seconds)"""
  _timer = min(max(int(time*100),0),255)
  transmit(direction=1, speed=int(31 * (velocity/3)), timer=_timer)

def right(velocity:int = 3, time:float = 0) -> None:
  """Tells the servos to go right
   \nspeed:int [0,3]
   \ntimer:float [0, 2.55] (seconds)"""
  _timer = min(max(int(time*100),0),255)
  transmit(direction=2, speed=int(31 * (velocity/3)), timer=_timer)

def left(velocity:int = 3, time:float = 0) -> None:
  """Tells the servos to go left
   \nspeed:int [0,3]
   \ntimer:float [0, 2.55] (seconds)"""
  _timer = min(max(int(time*100),0),255)
  transmit(direction=3, speed=int(31 * (velocity/3)), timer=_timer)

def shutdown() -> None:
  """Runs shutdown sequence"""
  stop()
  #GPIO.cleanup()

def timedTurn():
  pass

if __name__ == "__main__":
  while True:
    val = input("Press Enter to send, direction, speed, time").split()
    transmit(int(val[0]), int(val[1]), int(val[2]))
    