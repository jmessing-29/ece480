import serial
import time


arduino = serial.Serial('/dev/tty.HC-05', 9600, timeout=.1)

while True:
  arduino.write('c'.encode('utf-8'))
  time.sleep(0.5)
  

  