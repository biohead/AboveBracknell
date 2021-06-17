#!/bin/bash

# This is just a simple script that loads the correct python enviroment
# and then loops forever restarting the tracker program if it ever exits.

cd /home/pi/AboveMonroe

while :
do
	echo
	echo "*** Starting [AboveMonroe] $(date) ***"
	echo

	python3 AircraftTracker.py

	echo
	echo "*** Exiting  [AboveMonroe] $(date) ***"
	echo

	sleep 5
done

