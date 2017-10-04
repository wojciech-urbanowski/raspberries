#!/usr/bin/python

import sys
import urllib2
import os
import time
import random

thingspeakapikey = sys.argv[1].strip()
initialsleep = int(sys.argv[2])
field = sys.argv[3]

if (initialsleep > 0):
	time.sleep(random.randint(0,initialsleep))

avgload = os.getloadavg()[1]
#print avgload
request = urllib2.urlopen("https://api.thingspeak.com/update?api_key=" + thingspeakapikey + "&field" + field + "=" + str(avgload))
request.read()
request.close()
