# Import Libs
import serial
import time

# Global Var
avr = serial.Serial('/dev/ttyUSB0', 9600)

# Functions
def getProximity():
	avr.write(b'S')
	val = avr.readline()
	print(val)

# Test Code
time.sleep(5)
getProximity()

