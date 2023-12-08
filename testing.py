import serial


arduino = serial.Serial('/dev/tty.HC-05', 9600, timeout=.1)

while True:
  if arduino.in_waiting > 0:
    print (arduino.readline().decode().strip())

  