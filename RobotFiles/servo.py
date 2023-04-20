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
  import RPi.GPIO as GPIO # type: ignore
else:
  import fake_rpi
  GPIO = fake_rpi.fake_rpi.RPi.GPIO

import time

# Sets up output pins for communication with arduino
triggerPin = 4
dataPins = [17, 18, 22, 23]

GPIO.setmode(GPIO.BCM)
GPIO.setup(triggerPin, GPIO.OUT)
[GPIO.setup(pin, GPIO.OUT) for pin in dataPins] # Setup all data pins as outputs

def transmit(direction = 0, speed = 0, timer = 0, pulseWidth: float = 12/1000):
  """Sends instructions to the arduino"""
  direction_bin = bin(direction + 1024)[-3:] # Get the three bits for direction
  speed_bin = bin(speed + 1024)[-5:] # Get the 5 bits for speed
  timer_bin = bin(timer + 1024)[-8:] # Get the 8 bits for duration

  # Combine bits into 2 byte list
  data = [int(i) for i in str(direction_bin)[::-1]] + [int(i) for i in str(speed_bin)[::-1]] + [int(i) for i in str(timer_bin)[::-1]]

  # Split data into 4 bit segments
  dataSplit = [] 
  for i in range(0, len(data)//4):
    dataSplit.append([data[j + 4*i] for j in range(4)])

  # Send interrupt to the arduino to start data transfer process
  GPIO.output(triggerPin, GPIO.HIGH)
  time.sleep(pulseWidth/2)
  GPIO.output(triggerPin, GPIO.LOW)

  # Transmit data
  for halfByte in dataSplit:
    for i in range(4):
      GPIO.output(dataPins[i], halfByte[i])
    time.sleep(pulseWidth)
  
  # Set all pins to low after transmission
  for pin in dataPins:
    GPIO.output(pin, GPIO.LOW)

def stop() -> None:
  """Tells the servos to stop"""
  transmit(direction=0, speed=0, timer=0)

def forward(velocity:int = 8, time:float = 0) -> None:
  """Tells the servos to go forward
   \nspeed:int [0,31]
   \ntimer:float [0, 2.55] (seconds)"""
  _velocity = min(max(velocity,0),31)
  _timer = min(max(int(time*100),0),255)
  transmit(direction=0, speed=_velocity, timer=_timer)

def backward(velocity:int = 8, time:float = 0) -> None:
  """Tells the servos to go backward
   \nspeed:int [0,31]
   \ntimer:float [0, 2.55] (seconds)"""
  _velocity = min(max(velocity,0),31)
  _timer = min(max(int(time*100),0),255)
  transmit(direction=1, speed=_velocity, timer=_timer)

def right(velocity:int = 8, time:float = 0) -> None:
  """Tells the servos to go right
   \nspeed:int [0,31]
   \ntimer:float [0, 2.55] (seconds)"""
  _velocity = min(max(velocity,0),31)
  _timer = min(max(int(time*100),0),255)
  transmit(direction=2, speed=_velocity, timer=_timer)

def left(velocity:int = 8, time:float = 0) -> None:
  """Tells the servos to go left
   \nspeed:int [0,31]
   \ntimer:float [0, 2.55] (seconds)"""
  _velocity = min(max(velocity,0),31)
  _timer = min(max(int(time*100),0),255)
  transmit(direction=3, speed=_velocity, timer=_timer)

def shutdown() -> None:
  """Runs shutdown sequence"""
  stop()
  #GPIO.cleanup()

def timedTurn(magnitude:float):
  timer = abs(magnitude)/4
  if (magnitude < 0):
    right(8,timer)
  elif (magnitude > 0):
    left(8, timer)
  else:
    stop()

def timedMove(magnitude:float):
  timer = abs(magnitude)
  if (magnitude < 0):
    backward(8,timer)
  elif (magnitude > 0):
    forward(8, timer)
  else:
    stop()

if __name__ == "__main__":
  while True:
    val = input("Press Enter to send, direction, speed, time").split()
    transmit(int(val[0]), int(val[1]), int(val[2]))
    
