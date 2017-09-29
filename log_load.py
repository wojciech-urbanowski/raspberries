#!/usr/bin/python

import urllib2
import os
import time
import random

thingspeakapikeyfile = open(sys.argv[1], "r")
thingspeakapikey = thingspeakapikeyfile.read().strip()
thingspeakapikeyfile.close()

time.sleep(random.randint(0,59))

avgload = os.getloadavg()[1]
print avgload
request = urllib2.urlopen("https://api.thingspeak.com/update?api_key=" + thingspeakapikey + "&field3=" + str(avgload))
request.read()
request.close()
