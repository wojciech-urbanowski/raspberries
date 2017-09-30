#!/usr/bin/python

import sys
import re
import subprocess
import urllib2
import random
import time

thingspeakapikey = sys.argv[1].strip()
initialsleep = int(sys.argv[2])
field = sys.argv[3].strip()

if (initialsleep > 0):
        time.sleep(random.randint(0,initialsleep))

content = subprocess.check_output(['/opt/vc/bin/vcgencmd', 'measure_temp'])
#print content
matchObj0 = re.search(r'temp=[0-9]*\.[0-9]*\'C', content)
#print matchObj0
if matchObj0:
	rawTemperature = matchObj0.group(0)[5:-2]
	temperature = float(rawTemperature)
	#print temperature
	request = urllib2.urlopen("https://api.thingspeak.com/update?api_key=" + thingspeakapikey + "&field" + field + "=" + str(temperature))
	request.read()
	request.close()
