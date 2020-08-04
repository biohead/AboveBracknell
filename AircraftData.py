"""
Aircraft Data.
"""

__author__ = "HariA"


import datetime
import logging
import logging.handlers
import os
import sys
import traceback

import Config
import Logger
import HelperModules


myLogger = logging.getLogger(Logger.sBaseFileName)


class FlightData:
    """
    Class FlightData
    """

    def __init__(
        self,
        aHex,
        aFlight,
        aAltitude,
        aHeading,
        aLatitude,
        aLongitude,
        aSpeed,
        aSquawk,
        aSeen,
        aDistance,
        aElevation,
        aOperator,
        aCountry,
        aCallsign,
        aEmergency,
        aFlags,
        aType,
    ):
        self.aHex = aHex
        self.aFlight = aFlight
        self.aAltitude = aAltitude
        self.aHeading = aHeading
        self.aLatitude = aLatitude
        self.aLongitude = aLongitude
        self.aSpeed = aSpeed
        self.aSquawk = aSquawk
        self.aSeen = aSeen
        self.aDistance = aDistance
        self.aElevation = aElevation
        self.aOperator = aOperator
        self.aCountry = aCountry
        self.aCallsign = aCallsign
        self.aEmergency = aEmergency
        self.aFlags = aFlags
        self.aType = aType

    def __repr__(self):
        return "%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s" % (
            self.aHex,
            self.aFlight,
            self.aAltitude,
            self.aHeading,
            self.aLatitude,
            self.aLongitude,
            self.aSpeed,
            self.aSquawk,
            self.aSeen,
            self.aDistance,
            self.aElevation,
            self.aOperator,
            self.aCountry,
            self.aCallsign,
            self.aEmergency,
            self.aFlags,
            self.aType,
        )

    @staticmethod
    def getFlights(flightData, myOperators, myAircrafts):
        """
        Get all valid flights
        """

        myFlights = []
        aID = ""

        try:
            for aCraft in flightData["aircraft"]:
                aHex = None
                aFlight = None
                aAltitude = 0
                aHeading = None
                aLatitude = 0
                aLongitude = 0
                aSpeed = 0
                aSquawk = None
                aSeen = 0
                aDistance = 0
                aElevation = 0
                aOperator = None
                aCountry = None
                aCallsign = None
                aEmergency = None
                aFlags = None
                aType = None

                if "lat" in aCraft:
                    aLatitude = float(aCraft["lat"]) if aCraft["lat"] else 0

                if "lon" in aCraft:
                    aLongitude = float(aCraft["lon"]) if aCraft["lon"] else 0

                if aLatitude and aLongitude:
                    if "hex" in aCraft:
                        aHex = (
                            aCraft["hex"].strip().replace("~", "").upper()
                            if aCraft["hex"]
                            else None
                        )

                    if "flight" in aCraft:
                        aFlight = (
                            aCraft["flight"].strip().upper()
                            if aCraft["flight"]
                            else None
                        )

                    if "alt_baro" in aCraft:
                        aAltitude = aCraft["alt_baro"]
                    elif "alt_geom" in aCraft:
                        aAltitude = aCraft["alt_geom"]
                    else:
                        aAltitude = 0

                    if "track" in aCraft:
                        aHeading = (
                            HelperModules.headingDirection(aCraft["track"])
                            if aCraft["track"]
                            else None
                        )

                    if "squawk" in aCraft:
                        aSquawk = aCraft["squawk"] if aCraft["squawk"] else None

                    if "seen" in aCraft:
                        aSeen = aCraft["seen"] if aCraft["seen"] else 0

                    if "gs" in aCraft:
                        aSpeed = HelperModules.knots2mph(aCraft["gs"])
                    elif "tas" in aCraft:
                        aSpeed = HelperModules.knots2mph(aCraft["tas"])
                    elif "ias" in aCraft:
                        aSpeed = HelperModules.knots2mph(aCraft["ias"])
                    elif "mach" in aCraft:
                        aSpeed = HelperModules.knots2mph(
                            HelperModules.mach2knots(aCraft["mach"])
                        )
                    else:
                        aSpeed = 0

                    aDistance = HelperModules.distanceFromAtoB(
                        (Config.lLatitude, Config.lLongitude), (aLatitude, aLongitude)
                    )

                    if aAltitude and aDistance:
                        aElevation = HelperModules.getElevation(aAltitude, aDistance)
                    else:
                        aElevation = 0

                    if "emergency" in aCraft and aCraft["emergency"] not in (
                        "",
                        "none",
                    ):
                        aEmergency = aCraft["emergency"]
                    else:
                        aEmergency = None

                    if aFlight:
                        aID = aFlight[0:3]

                        if aID in myOperators and aID.isalpha():
                            aOperator = myOperators[aID][0]
                            aCountry = myOperators[aID][1]
                            aCallsign = myOperators[aID][2]
                        else:
                            aOperator = None
                            aCountry = None
                            aCallsign = None

                    if aHex in myAircrafts:
                        aFlags = myAircrafts[aHex][0]

                        if myAircrafts[aHex][1][0:4].isdigit():
                            aTypeTokens = myAircrafts[aHex][1].split()
                            aType = "%s (%s)" % (
                                " ".join(aTypeTokens[1:]).upper(),
                                aTypeTokens[0],
                            )
                        else:
                            aType = myAircrafts[aHex][1].upper()
                    else:
                        aFlags = None
                        aType = None

                    aData = FlightData(
                        aHex,
                        aFlight,
                        aAltitude,
                        aHeading,
                        aLatitude,
                        aLongitude,
                        aSpeed,
                        aSquawk,
                        aSeen,
                        aDistance,
                        aElevation,
                        aOperator,
                        aCountry,
                        aCallsign,
                        aEmergency,
                        aFlags,
                        aType,
                    )

                    myFlights.append(aData)

            # sort by distance
            myFlights.sort(key=lambda aCraft: aCraft.aDistance)

        except Exception:
            myLogger.exception(
                "Exception in [file: %s | module: %s | line: %s]: %s",
                os.path.basename(traceback.extract_stack()[-1][0]),
                traceback.extract_stack()[-1][2],
                traceback.extract_stack()[-1][1],
                sys.exc_info()[1],
            )
            return None

        return myFlights

    @staticmethod
    def getTime(flightData):
        """
        Get json time
        """

        try:
            sTime = datetime.datetime.fromtimestamp((flightData["now"])).strftime(
                "%I:%M:%S %p"
            )

        except Exception:
            myLogger.exception(
                "Exception in [file: %s | module: %s | line: %s]: %s",
                os.path.basename(traceback.extract_stack()[-1][0]),
                traceback.extract_stack()[-1][2],
                traceback.extract_stack()[-1][1],
                sys.exc_info()[1],
            )
            return None

        return sTime
