#!/bin/bash

# The IP for the server you wish to ping
SERVER=$(/sbin/ip route | awk '/default/ { print $3 }')

# Specify wlan interface
WLANINTERFACE=wlan0

# Only send two pings, sending output to /dev/null
ping -I ${WLANINTERFACE} -c2 ${SERVER} > /dev/null

# If the return code from ping ($?) is not 0 (meaning there was an error)
if [ $? != 0 ]
then
	# Restart the wireless interface
	ifdown --force wlan0
	sleep 2
	ifup wlan0

	sleep 10

	ping -I ${WLANINTERFACE} -c2 ${SERVER} > /dev/null
	if [ $? != 0 ]
	then
		/sbin/shutdown -r now
	fi
fi
