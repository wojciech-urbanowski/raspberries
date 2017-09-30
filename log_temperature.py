#!/usr/bin/python

import sys
import re
import urllib2
import time
import random
from datetime import datetime
from threading import Thread

def keepcpubusy(keepbusy):
	start = datetime.now()
	now = start
        dummy = 0
        while(keepbusy[0]>0 and (now - start).total_seconds() <= 10):
                dummy = dummy + 1
                if (dummy > 1024):
                        dummy = 0
			now = datetime.now()

thingspeakapikey = sys.argv[1].strip()
initialsleep = int(sys.argv[2])
device = sys.argv[3].strip()
field = sys.argv[4].strip()

verbose = False
if (len(sys.argv) >= 6):
	if (len(sys.argv[5].strip()) > 0):
		verbose = True

if (initialsleep > 0):
	time.sleep(random.randint(0,initialsleep))

for dummy in range(10):
	time.sleep(1)

	keepbusy = [1];
	t = Thread(target=keepcpubusy, args=(keepbusy,))
	t.start()
	time.sleep(1)

	file = open("/sys/bus/w1/devices/" + device + "/w1_slave", "r")
	content = file.read()
	file.close()

	keepbusy[0] = 0
	t.join()

	contentLines = content.splitlines()
	if (len(contentLines) == 2):
		if (verbose):
			print contentLines
		line0 = contentLines[0]
		#print line0
		matchObj0 = re.search(r'crc=[0-9a-f]+\sYES', line0)
		#print matchObj0
		if matchObj0:
			line1 = contentLines[1]
			matchObj1 = re.search(r't=[0-9]+', line1)
			#print matchObj1
			if matchObj1:
				rawTemperature = matchObj1.group(0)[2:]
				temperature = float(rawTemperature)/1000
				#print temperature
				#print "https://api.thingspeak.com/update?api_key=" + thingspeakapikey + "&field1=" + str(temperature)
				request = urllib2.urlopen("https://api.thingspeak.com/update?api_key=" + thingspeakapikey + "&field" + field + "=" + str(temperature))
				request.read()
				request.close()
				break

