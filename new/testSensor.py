# Import Libs
import serial


# Function to pick Max of 100 Readings
def getProximity():
	with serial.Serial('/dev/ttyUSB0', 9600, timeout = 1) as prox:
		prox.write('S');
		print(prox.readline());
