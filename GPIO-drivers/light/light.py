import spidev
import time
import os

# Open SPI bus and define channels
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=1000000

light_channel = 0

# Delay between readings
delay = 1

# Function to read SPI data from MCP3008 chop
# Channel must be integer 0-7

def ReadChannel(channel):
	adc = spi.xfer2([1,(8+channel)<<4,0])
	data = ((adc[1]&3) << 8) + adc[2]
	return data
	
# Function to convert data to voltage level
# Round 4 decimal places
def ConvertVolts(data):
	volts = (data * 3.3) / float(1023)
	volts = round(volts, 4)
	return volts
	
# Main function
while True:

	# Readings tend to fluctuate to max of 1023
	# Taking average of 100 readings and excluding max from average
	num_readings = 0
	sum_light_readings = 0.0
	while(num_readings < 100):
		current_read = ReadChannel(light_channel)
		if(current_read != 1023.0):
			sum_light_readings = sum_light_readings + current_read
			num_readings = num_readings + 1
	
	light_level = sum_light_readings / num_readings
	light_volts = ConvertVolts(light_level)
	
	# Print results
	print("***********************************************")
	print("Light: {} ({}V)".format(light_level,light_volts))
	
	time.sleep(delay)
