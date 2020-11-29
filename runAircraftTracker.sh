#!/bin/bash

# This is just a simple script that loads the correct python enviroment
# and then loops forever restarting the tracker program if it ever exits.


cd /home/pi/AboveBracknell

while :
do
	echo
	echo "*** Starting [AboveBracknell] $(date) ***"
	echo

	python3 AircraftTracker.py

	echo
	echo "*** [AboveBracknell] exited $(date) ***"
	echo

	sleep 5
done

