# Fake rpi library used instead of RPi.GPIO for debugging on
# a system other then the raspberry pi
import serial
import serial.tools.list_ports
import io
import os

def find_arduino(port=None):
    """Get the name of the port that is connected to Arduino."""
    if port is None:
        ports = serial.tools.list_ports.comports()
        for p in ports:
            if p.manufacturer is not None and "Arduino" in p.manufacturer:
                port = p.device
    return port

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
from gpiozero import DistanceSensor


US_TRIGGER = 23
US_ECHO = 24

ultrasonic = DistanceSensor(US_ECHO, US_TRIGGER, max_distance=5)


def _initialize() -> bool:
  """Connects to arduino, returns true if succeeded"""
  for _ in range(5):
    try:
      global port, arduino
      port = find_arduino()
      arduino = serial.Serial(port, baudrate=9600)
      return True
    except:
      pass
  return False

if not _initialize(): # Throw error if failed to connect to arduino
  raise Exception("Failed to establish connection to arduino")

GPIO.setmode(GPIO.BCM)


def transmit(direction = 0, speed = 0, timer = 0, DEBUG = False):
  _speed = min(max(speed,0),31)
  _timer = min(max(int(timer*100),0),255)
  try:
    """Sends instructions to the arduino"""
    arduino.write(bytes([_timer, _speed, direction])) # Write instructions
    time.sleep(.05)
    if DEBUG:
      print(bytes([_timer, _speed, direction]))      
      re = arduino.read_all()
      
      print("Response: " + re.decode())
    else:
      _ = arduino.read_all() # Clear buffer
  except Exception as ex: # If error occurred try to reconnect to arduino
    print("Error thrown: " + ex)
    if not _initialize():
      raise Exception("Failed to establish connection to arduino")
  
def stop() -> None:
  """Tells the servos to stop"""
  transmit(direction=0, speed=0, timer=0)

def forward(speed:int = 16, timer:float = 0) -> None:
  """Tells the servos to go forward
   \nspeed:int [0,31]
   \ntimer:float [0, 2.55] (seconds)"""

  transmit(direction=0, speed=speed, timer=timer)

def backward(speed:int = 16, timer:float = 0) -> None:
  """Tells the servos to go backward
   \nspeed:int [0,31]
   \ntimer:float [0, 2.55] (seconds)"""
  transmit(direction=1, speed=speed, timer=timer)

def right(speed:int = 16, timer:float = 0) -> None:
  """Tells the servos to go right
   \nspeed:int [0,31]
   \ntimer:float [0, 2.55] (seconds)"""
  transmit(direction=2, speed=speed, timer=timer)

def left(speed:int = 16, timer:float = 0) -> None:
  """Tells the servos to go left
   \nspeed:int [0,31]
   \ntimer:float [0, 2.55] (seconds)"""
  transmit(direction=3, speed=speed, timer=timer)

def shutdown() -> None:
  """Runs shutdown sequence"""
  stop()
  arduino.close()
  #GPIO.cleanup()

def timedTurn(magnitude:float, speed:int = 16):
  """Turns for a set time based on the magnitude of a float,
  positive turns left, negative turns right"""
  timer = abs(magnitude)/3
  if (magnitude < 0):
    right(speed,timer)
  elif (magnitude > 0):
    left(speed, timer)
  else:
    stop()

def timedMove(magnitude:float, speed:int = 16):
  """Moves for a set time based on the magnitude of a float,
  positive moves backward, negative turns moves forward"""
  timer = abs(magnitude)
  if (magnitude < 0):
    backward(speed,timer)
  elif (magnitude > 0):
    forward(speed, timer)
  else:
    stop()

def moveUntil(distance:float):
  forward(16, 0)
  while( ultraDistance() >= distance):
    print(ultraDistance())
  stop()

def ultraDistance():
  return ultrasonic.distance

if __name__ == "__main__":
  while True:
    try:
      val = input("Press Enter to send, direction, speed, time").split()
      transmit(int(val[0]), int(val[1]), int(val[2]))
    except Exception as ex:
      if type(ex) == KeyboardInterrupt:
        break
      stop()
    print(ultraDistance())
    
