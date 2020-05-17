#!/bin/bash
#
# This is just a simple script that loads the correct python enviroment
# and then loops forever restarting the tracker program if it ever exits.
#

cd /home/hari/Documents/AboveMonroeBot

while :
do
	echo
	echo "*** Starting [AboveMonroe] $(date) ***"
	echo

	python3 AircraftTracker.py

	echo
	echo "*** [AboveMonroe] exited $(date) ***"
	echo

	sleep 5
done
