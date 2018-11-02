import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library 
from time import sleep # Import the sleep function from the time module 
GPIO.setwarnings(False) # Ignore warning for now 
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering 
GPIO.setup(11, GPIO.OUT, initial=GPIO.LOW) # Set pin 8 to be an output pin and set initial value to low (off) 
def ledON():
	GPIO.output(11, GPIO.HIGH) # Turn on
def ledOFF():
	GPIO.output(11, GPIO.LOW) # Turn off
