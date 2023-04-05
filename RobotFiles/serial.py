from serial import Serial
from time import strftime, time, localtime, sleep

def write(s, t=None):
  if t is None:
    t = strftime('s%H:%M:%S', localtime(time() + 1)).encode('ascii')
  else:
    t = ('s%s' % t).encode('ascii')
  s.write(t)
  while int(time()%1*1000): pass # wait for ms to be 0
  s.write(b'\r')
  print(t)

if __name__ == '__main__':
  from sys import argv
  s = Serial('/dev/ttyAMA0')
  for i in range(3):
    write(s, None if len(argv)<2 else argv[1])
    sleep(.1)