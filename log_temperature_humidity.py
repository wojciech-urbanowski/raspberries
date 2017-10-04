#!/usr/bin/python

import sys
import re
import urllib2
import time
import random
from datetime import datetime
from threading import Thread

import Adafruit_DHT

#def keepcpubusy(keepbusy):
#	start = datetime.now()
#	now = start
#        dummy = 0
#        while(keepbusy[0]>0 and (now - start).total_seconds() <= 10):
#                dummy = dummy + 1
#                if (dummy > 1024):
#                        dummy = 0
#			now = datetime.now()

thingspeakapikey = sys.argv[1].strip()
initialsleepoffset = int(sys.argv[2])
initialsleep = int(sys.argv[3])
fieldTemp = sys.argv[4].strip()
fieldHumid = sys.argv[5].strip()
dhtgpio = int(sys.argv[6])

verbose = False
if (len(sys.argv) >= 8):
	if (len(sys.argv[7].strip()) > 0):
		verbose = True

if (initialsleepoffset > 0 or initialsleep > 0):
	time.sleep(initialsleepoffset + random.randint(0,initialsleep))

for dummy in range(10):
	time.sleep(1)

#	keepbusy = [1];
#	t = Thread(target=keepcpubusy, args=(keepbusy,))
#	t.start()
#	time.sleep(1)

	if (verbose):
		print "Pin:"
		print dhtgpio

	humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, dhtgpio)

#	keepbusy[0] = 0
#	t.join()

	if (verbose):
		print humidity
		print temperature

	if humidity is not None and temperature is not None:
		request = urllib2.urlopen("https://api.thingspeak.com/update?api_key=" + thingspeakapikey + "&field" + fieldTemp + "=" + str(temperature) + "&field" + fieldHumid + "=" + str(humidity))
		request.read()
		request.close()
		break

