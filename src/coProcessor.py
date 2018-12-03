# Import Libs
import serial
import time

# Global Var
avr = None
dly = 2

# Functions
def initProximity():
	global avr
	avr = serial.Serial('/dev/ttyUSB0', 9600)
	time.sleep(dly)
	
def getProximity():
	avr.write(b'S')
	val = int(avr.readline())
	return val

def setLedWhiteFadeIn():
	avr.write(b'A')

def setLedWhiteFadeOut():
	avr.write(b'B')


# Test Code
#initProximity()
#while(1):
#	getProximity()
