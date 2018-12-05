# Import Libs
import serial
import time

# Global Var
avr = None
dly = 2
adly = 0.25

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
	time.sleep(adly)

def setLedWhiteFadeOut():
	avr.write(b'B')
	time.sleep(adly)

def setLedGreenFadeIn():
	avr.write(b'C')
	time.sleep(adly)

def setLedGreenFadeOut():
	avr.write(b'D')
	time.sleep(adly)


# Test Code
#initProximity()
#setLedWhiteFadeIn()

