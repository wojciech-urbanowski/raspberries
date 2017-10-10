#!/usr/bin/python

import sys
import re
import urllib2
import time
import random
import subprocess
import os
from datetime import datetime
from threading import Thread

import Adafruit_DHT

thingspeakapikey = sys.argv[1].strip()
initialsleepoffset = int(sys.argv[2])
initialsleep = int(sys.argv[3])
fieldTemp = sys.argv[4].strip()
fieldHumid = sys.argv[5].strip()
fieldCPUTemp = sys.argv[6].strip()
fieldLoad = sys.argv[7].strip()
dhtgpio = int(sys.argv[8])

verbose = False
if (len(sys.argv) >= 10):
	if (len(sys.argv[9].strip()) > 0):
		verbose = True

if (initialsleepoffset > 0 or initialsleep > 0):
	time.sleep(initialsleepoffset + random.randint(0,initialsleep))

cpuTemperatureContent = subprocess.check_output(['/opt/vc/bin/vcgencmd', 'measure_temp'])
avgload = os.getloadavg()[1]

cpuTemperatureMatchObj0 = re.search(r'temp=[0-9]*\.[0-9]*\'C', cpuTemperatureContent)
cpuTemperature = 0.0
if cpuTemperatureMatchObj0:
        rawCPUTemperature = cpuTemperatureMatchObj0.group(0)[5:-2]
        cpuTemperature = float(rawCPUTemperature)

for dummy in range(10):
	time.sleep(1)

	humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, dhtgpio)

	if (verbose):
		print humidity
		print temperature

	if humidity is not None and temperature is not None:
		request = urllib2.urlopen("https://api.thingspeak.com/update?api_key=" + thingspeakapikey + "&field" + fieldTemp + "=" + str(temperature) + "&field" + fieldHumid + "=" + str(humidity) + "&field" + fieldCPUTemp + "=" + str(cpuTemperature) + "&field" + fieldLoad + "=" + str(avgload))
		request.read()
		request.close()
		break

