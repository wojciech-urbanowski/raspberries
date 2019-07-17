#!/usr/bin/python3

import sys
import re
import subprocess
import random
import time
import datetime
from urllib.request import urlopen

thingspeakapikey = sys.argv[1].strip()
initialsleep = int(sys.argv[2])
field = sys.argv[3].strip()
sleepbetween = int(sys.argv[4].strip())

if (initialsleep > 0):
        time.sleep(random.randint(0,initialsleep))

today = datetime.date.today().day

lastReading = -1

while today == datetime.date.today().day:
	content = subprocess.check_output(['/opt/vc/bin/vcgencmd', 'measure_temp']).decode()
	#print(content)
	matchObj0 = re.search(r'temp=[0-9]*\.[0-9]*\'C', content)
	#print matchObj0
	if matchObj0:
		rawTemperature = matchObj0.group(0)[5:-2]
		temperature = float(rawTemperature)
		#print(temperature)
		if lastReading != temperature:
			request = urlopen("https://api.thingspeak.com/update?api_key=" + thingspeakapikey + "&field" + field + "=" + str(temperature))
			request.read()
			request.close()
			lastReading = temperature
	time.sleep(sleepbetween - 10 + random.randint(0, 20))
