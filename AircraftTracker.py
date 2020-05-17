"""
Aircraft Tracker.
"""

__author__ = "HariA"


import os
import sys
import threading
import time
import traceback

import Config
import Logger
import HelperModules
import AircraftData


def main(sKey, sValue):
    """
    Main module.
    """

    currentFlights = []
    previousFlights = []
    myOperators = []
    myAircrafts = []
    alarmFlights = {}
    nCount = 0
    bFound = False
    bScreenshot = False
    sStatus = ""
    fileName = os.path.splitext(os.path.basename(sys.argv[0]))[0]

    try:
        myLogger.debug("::: %s [Begin] :::", fileName, extra={"MHz": "[%s]" % (sKey)})

        previousReloadTime = time.time()
        myBrowser = HelperModules.openBrowser(sKey, sValue[0], sValue[2])

        # load operators.json and aircrafts.json once
        myOperators = HelperModules.getOperators()
        myAircrafts = HelperModules.getAircrafts()

        # initial aircraft.json load
        flightData = HelperModules.loadFlightData(sKey, sValue[1])
        currentFlights = AircraftData.FlightData.getFlights(flightData, myOperators, myAircrafts)
        previousFlights = currentFlights.copy()

        previousTime = AircraftData.FlightData.getTime(flightData)
        myLogger.debug("Time [%s] Current Flights [%3s]", previousTime[:-3], len(currentFlights), extra={"MHz": "[%s]" % sKey})

        while True:
            if time.time() > previousReloadTime + 3600 and not alarmFlights:
                myLogger.debug("Reloading browser after [1] hour", extra={"MHz": "[%s]" % sKey})
                myBrowser.quit()
                myBrowser = HelperModules.openBrowser(sKey, sValue[0], sValue[2])
                previousReloadTime = time.time()

            # load aircrafts
            time.sleep(Config.sleepTime)
            flightData = HelperModules.loadFlightData(sKey, sValue[1])
            currentFlights = AircraftData.FlightData.getFlights(flightData, myOperators, myAircrafts)

            # make sure you preserve aFlight in case the next json does not provide it.
            for nIndex1, aCraft1 in enumerate(currentFlights):
                for nIndex2, aCraft2 in enumerate(previousFlights):
                    if aCraft1.aHex == aCraft2.aHex:
                        if not aCraft1.aFlight and aCraft2.aFlight:
                            currentFlights[nIndex1].aFlight = aCraft2.aFlight
                            currentFlights[nIndex1].aOperator = aCraft2.aOperator
                            currentFlights[nIndex1].aCountry = aCraft2.aCountry
                            currentFlights[nIndex1].aCallsign = aCraft2.aCallsign

            previousFlights = currentFlights.copy()

            currentTime = AircraftData.FlightData.getTime(flightData)
            if currentTime == previousTime:
                continue

            previousTime = currentTime

            nCount += 1
            if nCount % 60 == 0:
                myLogger.debug("Time [%s] Current Flights [%3s]", previousTime[:-3], len(currentFlights), extra={"MHz": "[%s]" % sKey})
                nCount = 0

            dCurrentFlights = {}

            for aCraft in currentFlights:
                if aCraft.aDistance <= Config.distanceAlarm or aCraft.aElevation >= Config.elevationAlarm:
                    dCurrentFlights[aCraft.aHex] = aCraft

                    if aCraft.aHex in alarmFlights:
                        if aCraft.aDistance <= alarmFlights[aCraft.aHex][0].aDistance:
                            alarmFlights[aCraft.aHex] = (aCraft, 0)
                    else:
                        alarmFlights[aCraft.aHex] = (aCraft, 0)

            lFinishedAlarms = []
            for aHex1, aCraft1 in alarmFlights.items():
                bFound = False
                for aHex2, aCraft2 in dCurrentFlights.items():
                    if aHex1 == aHex2:
                        if aCraft1[0].aDistance <= Config.distanceAlarm:
                            myLogger.debug("[%s|%s] is [%s] miles away [%s]", aHex1, aCraft1[0].aFlight, aCraft1[0].aDistance, previousTime, extra={"MHz": "[%s]" % sKey})
                        else:
                            myLogger.debug("[%s|%s] is at [%s%s] elevation [%s]", aHex1, aCraft1[0].aFlight, aCraft1[0].aElevation, u"\N{DEGREE SIGN}", previousTime, extra={"MHz": "[%s]" % sKey})

                        bFound = True
                        break

                if not bFound:
                    if aCraft1[1] < Config.waitXUpdates:
                        alarmFlights[aHex1] = (aCraft1[0], aCraft1[1] + 1)
                    else:
                        myLogger.debug("Taking screenshot of [%s|%s]", aHex1, aCraft1[0].aFlight, extra={"MHz": "[%s]" % sKey})
                        if myBrowser:
                            bScreenshot = HelperModules.getScreenshot(sKey, myBrowser, aHex1)

                        if bScreenshot:
                            sStatus = HelperModules.formStatus(sKey, aCraft1[0], previousTime)

                            tObject = threading.Thread(name="%s|%s" % (aHex1, aCraft1[0].aFlight), target=HelperModules.tweetNow, args=(sKey, "{}.png".format(aHex1), sStatus), daemon=True)
                            myLogger.debug("Starting thread [%s] daemon [%s]", tObject.name, tObject.daemon, extra={"MHz": "[%s]" % sKey})
                            tObject.start()

                        lFinishedAlarms.append(aHex1)

            for aHex in lFinishedAlarms:
                del alarmFlights[aHex]

        myLogger.debug("::: %s [ End ] :::\n", fileName, extra={"MHz": "[%s]" % sKey})

    except Exception:
        myLogger.debug("Exception in [file: %s | module: %s | line: %s]: %s", os.path.basename(traceback.extract_stack()[-1][0]), traceback.extract_stack()[-1][2], traceback.extract_stack()[-1][1], sys.exc_info()[1], extra={"MHz": "[%s]" % sKey})
        myBrowser.quit()
        return False

    return False


if __name__ == "__main__":

    status = 0

    myLogger = Logger.setLogger()

    for sKey, sValue in Config.dURL.items():
        tObject = threading.Thread(name="%s" % (sKey), target=main, args=(sKey, sValue), daemon=False)
        tObject.start()

    tObject.join()

    sys.exit(0)

