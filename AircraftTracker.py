"""
Aircraft Tracker.
"""

__author__ = "HariA"


import os
import sys
import time
import traceback

import Config
import Logger
import HelperModules
import AircraftData


def main():
    """
    Main module.
    """

    currentFlights = []
    previousFlights = []
    myOperators = []
    myAircrafts = []
    alarmFlights = {}
    cCount = 0
    tCount = 0
    bFound = False
    bScreenshot = False
    sStatus = ""

    try:
        previousReloadTime = time.time()
        myBrowser = HelperModules.openBrowser()

        while myBrowser is None:
            myLogger.debug("Reloading browser after crash")
            myBrowser = HelperModules.openBrowser()

        # load operators.json and aircrafts.json once
        myOperators = HelperModules.getOperators()
        myAircrafts = HelperModules.getAircrafts()

        # initial aircraft.json load
        flightData = HelperModules.loadFlightData()
        currentFlights = AircraftData.FlightData.getFlights(
            flightData, myOperators, myAircrafts
        )
        previousFlights = currentFlights.copy()

        previousTime = AircraftData.FlightData.getTime(flightData)
        myLogger.debug(
            "Coverage [%s mi | %s%s elevation]",
            Config.distanceAlarm,
            Config.elevationAlarm,
            u"\N{DEGREE SIGN}",
        )
        myLogger.debug(
            "[%3s] flights @ [%s]",
            len(currentFlights),
            previousTime,
        )

        while True:
            if (
                time.time() > previousReloadTime + Config.reloadTime
                and not alarmFlights
            ):
                myLogger.debug(
                    "Reloading browser after [%s] hour(s)",
                    int(Config.reloadTime / (60 * 60)),
                )

                if not isinstance(myBrowser, (bool)):
                    myBrowser.quit()

                myBrowser = HelperModules.openBrowser()

                while myBrowser is None:
                    myLogger.debug("Reloading browser after crash")
                    myBrowser = HelperModules.openBrowser()

                previousReloadTime = time.time()

                myLogger.debug(
                    "Coverage [%smi | %s%s elevation]",
                    Config.distanceAlarm,
                    Config.elevationAlarm,
                    u"\N{DEGREE SIGN}",
                )

            # load aircrafts
            time.sleep(Config.sleepTime)
            flightData = HelperModules.loadFlightData()
            currentFlights = AircraftData.FlightData.getFlights(
                flightData, myOperators, myAircrafts
            )

            # make sure you preserve aFlight in case the next json does not provide it.
            for nIndex1, aCraft1 in enumerate(currentFlights):
                for nIndex2, aCraft2 in enumerate(previousFlights):
                    if aCraft1.aFlight == aCraft2.aFlight:
                        if not aCraft1.aHex and aCraft2.aHex:
                            currentFlights[nIndex1].aFlight = aCraft2.aFlight
                            currentFlights[nIndex1].aOperator = aCraft2.aOperator
                            currentFlights[nIndex1].aCountry = aCraft2.aCountry
                            currentFlights[nIndex1].aCallsign = aCraft2.aCallsign

            previousFlights = currentFlights.copy()

            currentTime = AircraftData.FlightData.getTime(flightData)
            if currentTime == previousTime:
                continue

            previousTime = currentTime

            cCount += 1
            if cCount % Config.checkEveryXTime == 0:
                myLogger.debug(
                    "[%3s] flights @ [%s]",
                    len(currentFlights),
                    previousTime,
                )
                cCount = 0

            dCurrentFlights = {}

            for aCraft in currentFlights:
                if (
                    aCraft.aDistance <= Config.distanceAlarm
                    or aCraft.aElevation >= Config.elevationAlarm
                ):
                    dCurrentFlights[aCraft.aFlight] = aCraft

                    if aCraft.aHex in alarmFlights:
                        if aCraft.aDistance <= alarmFlights[aCraft.aHex][0].aDistance:
                            alarmFlights[aCraft.aFlight] = (aCraft, 0)
                    else:
                        alarmFlights[aCraft.aFlight] = (aCraft, 0)

            lFinishedAlarms = []
            for aFlight1, aCraft1 in alarmFlights.items():
                bFound = False
                tCount += 1
                for aFlight2, aCraft2 in dCurrentFlights.items():
                    if aFlight1 == aFlight2:
                        if cCount % Config.trackEveryXTime == 0:
                            myLogger.debug(
                                "Tracking [%s|%s]",
                                aFlight1,
                                aCraft1[0].aFlight,
                            )
                            tCount = 0
                        bFound = True
                        break

                if not bFound:
                    if aCraft1[1] < Config.waitXUpdates:
                        alarmFlights[aFlight1] = (aCraft1[0], aCraft1[1] + 1)
                    else:
                        if myBrowser is not None:
                            bScreenshot = HelperModules.getScreenshot(myBrowser, aFlight1)

                        if bScreenshot is not None:
                            sStatus = HelperModules.formStatus(
                                aCraft1[0], len(currentFlights), previousTime
                            )

                            HelperModules.tweetNow("%s.png" % (aFlight1), sStatus)

                        lFinishedAlarms.append(aFlight1)

            for aFlight in lFinishedAlarms:
                del alarmFlights[aFlight]

    except Exception:
        myLogger.exception(
            "Exception in [file: %s | module: %s | line: %s]: %s",
            os.path.basename(traceback.extract_stack()[-1][0]),
            traceback.extract_stack()[-1][2],
            traceback.extract_stack()[-1][1],
            sys.exc_info()[1],
        )

        if not isinstance(myBrowser, (bool)):
            myBrowser.quit()

        return True

    return False


if __name__ == "__main__":

    status = 0
    tObjects = []
    myLogger = Logger.setLogger()
    currentFile = os.path.splitext(os.path.basename(sys.argv[0]))[0]

    myLogger.debug("")
    myLogger.debug("*** %s [Begin] ***", currentFile)

    status = main()

    myLogger.debug("***  %s [End]  ***", currentFile)

    sys.exit(status)
