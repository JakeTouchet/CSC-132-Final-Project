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

US_TRIGGER = 24
US_ECHO = 27

# Ultra Sonic Constants
SETTLE_TIME = 2 # seconds to let the sensor settle
CALIBRATIONS = 5 # number of calibration measurements to take
CALIBRATION_DELAY = 1 # seconds to delay in between calibration measurements
TRIGGER_TIME = 0.00001 # seconds needed to trigger the sensor
SPEED_OF_SOUND = 343 # Speed of sound m/s

GPIO.setmode(GPIO.BCM)
GPIO.setup(triggerPin, GPIO.OUT)
[GPIO.setup(pin, GPIO.OUT) for pin in dataPins] # Setup all data pins as outputs
GPIO.setup(US_TRIGGER, GPIO.OUT)
GPIO.setup(US_ECHO, GPIO.IN)


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

def forward(velocity:int = 16, time:float = 0) -> None:
  """Tells the servos to go forward
   \nspeed:int [0,31]
   \ntimer:float [0, 2.55] (seconds)"""
  _velocity = min(max(velocity,0),31)
  _timer = min(max(int(time*100),0),255)
  transmit(direction=0, speed=_velocity, timer=_timer)

def backward(velocity:int = 16, time:float = 0) -> None:
  """Tells the servos to go backward
   \nspeed:int [0,31]
   \ntimer:float [0, 2.55] (seconds)"""
  _velocity = min(max(velocity,0),31)
  _timer = min(max(int(time*100),0),255)
  transmit(direction=1, speed=_velocity, timer=_timer)

def right(velocity:int = 16, time:float = 0) -> None:
  """Tells the servos to go right
   \nspeed:int [0,31]
   \ntimer:float [0, 2.55] (seconds)"""
  _velocity = min(max(velocity,0),31)
  _timer = min(max(int(time*100),0),255)
  transmit(direction=2, speed=_velocity, timer=_timer)

def left(velocity:int = 16, time:float = 0) -> None:
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

def timedTurn(magnitude:float, speed:int = 16):
  """Turns for a set time based on the magnitude of a float,
  positive turns left, negative turns right"""
  timer = abs(magnitude)/4
  if (magnitude < speed):
    right(8,timer)
  elif (magnitude > speed):
    left(8, timer)
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

def getDistance(correction_factor = 1):
  # trigger the sensor by setting it high for a short time and
  # then setting it low
  GPIO.output(US_TRIGGER, GPIO.HIGH)
  time.sleep(TRIGGER_TIME)
  GPIO.output(US_TRIGGER, GPIO.LOW)

  # wait for the ECHO pin to read high
  # once the ECHO pin is high, the start time is set
  # once the ECHO pin is low again, the end time is set
  while (GPIO.input(US_ECHO) == GPIO.LOW):
    start = time.time()
  while (GPIO.input(US_ECHO) == GPIO.HIGH):
    end = time.time()
  
  # calculate the duration that the ECHO pin was high
  # this is how long the pulse took to get from the sensor to
  # the object -- and back again
  duration = end - start
  # calculate the total distance that the pulse traveled by
  # factoring in the speed of sound (m/s)
  distance = duration * SPEED_OF_SOUND
  # the distance from the sensor to the object is half of the
  # total distance traveled
  distance /= 2
  # convert from meters to centimeters
  distance *= 100
  return distance * correction_factor


def calibrate(known_distance):
  # measure the distance to the object with the sensor
  # do this several times and get an average
  distance_avg = 0
  for i in range(CALIBRATIONS):
    distance = getDistance(1)
    if (False):
      print(f"--Got {distance}cm")
    # keep a running sum
    distance_avg += distance
    # delay a short time before using the sensor again
    time.sleep(CALIBRATION_DELAY)
  # calculate the average of the distances
  distance_avg /= CALIBRATIONS
  if (False):
    print(f"--Average is {distance_avg}cm")
  # calculate the correction factor
  correction_factor = known_distance / distance_avg
  if (False):
    print(f"--Correction factor is {correction_factor}")
  return correction_factor

if __name__ == "__main__":
  while True:
    val = input("Press Enter to send, direction, speed, time").split()
    transmit(int(val[0]), int(val[1]), int(val[2]))
    
