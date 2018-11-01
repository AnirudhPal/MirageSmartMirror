# Import Libs
import board
import busio
import adafruit_apds9960.apds9960

# I2C and Sensor Object
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_apds9960.apds9960.APDS9960(i2c)

# Samples
SAMPLE_NUM = 100

# Enable Proximity
sensor.enable_proximity = True

# Function to pick Max of 100 Readings
def getProximity(): 
	# Stores Max Value
	max = 0

	# Get Samples
	for x in range(SAMPLE_NUM):
		# Get Value
		val = sensor.proximity()

		# Update if Max
		if(val > max):
			max = val
	
	# Return Max
	return max

while(1):
	print(getProximity())


