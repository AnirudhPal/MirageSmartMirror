# Import Libs
import board
import busio
import adafruit_apds9960.apds9960

# Define I2C Interfcae
i2c = busio.I2C(board.SCL, board.SDA)

# Define Sensor
sensor = adafruit_apds9960.apds9960.APDS9960(i2c)

# Turn On Proximity
sensor.enable_proximity = True

# Get Proximity
sensor.proximity()
