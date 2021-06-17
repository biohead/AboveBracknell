"""
Helper Modules.
"""

__author__ = "HariA"


import decimal
import json
import logging
import logging.handlers
import math
import os
import sys
import time
import traceback

from io import BytesIO
from urllib.request import urlopen

import flag
import twython
from PIL import Image
from selenium import webdriver
from selenium.common import exceptions as SE
from selenium.webdriver.chrome.options import Options as SO
from selenium.webdriver.common.by import By as BY
from selenium.webdriver.support import expected_conditions as SC
from selenium.webdriver.support.wait import WebDriverWait as SW
from selenium.webdriver.common.action_chains import ActionChains as AC

import Config
import Logger


myLogger = logging.getLogger(Logger.sBaseFileName)


def headingDirection(headingTrack):
    """
    Get cardinal direction from degrees.
    """

    try:
        if not isinstance(headingTrack, (int, float, decimal.Decimal)):
            return False

        directionList = [
            "N",
            "NNE",
            "NE",
            "ENE",
            "E",
            "ESE",
            "SE",
            "SSE",
            "S",
            "SSW",
            "SW",
            "WSW",
            "W",
            "WNW",
            "NW",
            "NNW",
        ]

        sValue = int(math.floor((headingTrack / 22.5) + 0.5))
        sDirection = directionList[(sValue % 16)]

    except Exception:
        myLogger.exception(
            "Exception in [file: %s | module: %s | line: %s]: %s",
            os.path.basename(traceback.extract_stack()[-1][0]),
            traceback.extract_stack()[-1][2],
            traceback.extract_stack()[-1][1],
            sys.exc_info()[1],
        )
        return None

    return sDirection


def distanceFromAtoB(pA, pB):
    """
    Calculate the great circle distance between two points on the earth (specified in decimal degrees)

    http://stackoverflow.com/questions/15736995/how-can-i-quickly-estimate-the-distance-between-two-latitude-longitude-points
    """

    earthRadius = 3956

    try:
        if not isinstance(pA, tuple) or not isinstance(pB, tuple):
            return False

        if not isinstance(pA[0], (int, float, decimal.Decimal)):
            return False

        if not isinstance(pA[1], (int, float, decimal.Decimal)):
            return False

        if not isinstance(pB[0], (int, float, decimal.Decimal)):
            return False

        if not isinstance(pB[1], (int, float, decimal.Decimal)):
            return False

        latitudeOne, longitudeOne, latitudeTwo, longitudeTwo = map(
            math.radians, [pA[0], pA[1], pB[0], pB[1]]
        )

        dLatitude = latitudeTwo - latitudeOne
        dLongitude = longitudeTwo - longitudeOne

        a = (
            math.sin(dLatitude / 2) ** 2
            + math.cos(latitudeOne)
            * math.cos(latitudeTwo)
            * math.sin(dLongitude / 2) ** 2
        )
        c = 2 * math.asin(math.sqrt(a))

        nDistance = round(earthRadius * c, 1)

    except Exception:
        myLogger.exception(
            "Exception in [file: %s | module: %s | line: %s]: %s",
            os.path.basename(traceback.extract_stack()[-1][0]),
            traceback.extract_stack()[-1][2],
            traceback.extract_stack()[-1][1],
            sys.exc_info()[1],
        )
        return None

    return nDistance


def getElevation(aAltitude, aDistance):
    """
    Get the Elevation given Altitude and Distance.
    """

    try:
        if not isinstance(aAltitude, (int, float, decimal.Decimal)):
            return False

        if not isinstance(aDistance, (int, float, decimal.Decimal)):
            return False

        nElevation = round(math.degrees(math.atan(aAltitude / (aDistance * 5280))), 1)

    except Exception:
        myLogger.exception(
            "Exception in [file: %s | module: %s | line: %s]: %s",
            os.path.basename(traceback.extract_stack()[-1][0]),
            traceback.extract_stack()[-1][2],
            traceback.extract_stack()[-1][1],
            sys.exc_info()[1],
        )
        return None

    return nElevation


def knots2mph(aSpeed):
    """
    Converts knots to mph.
    """

    try:
        if not isinstance(aSpeed, (int, float, decimal.Decimal)):
            return False

        nSpeed = int(round(aSpeed * 1.15078, 0))

    except Exception:
        myLogger.exception(
            "Exception in [file: %s | module: %s | line: %s]: %s",
            os.path.basename(traceback.extract_stack()[-1][0]),
            traceback.extract_stack()[-1][2],
            traceback.extract_stack()[-1][1],
            sys.exc_info()[1],
        )
        return None

    return nSpeed


def mach2knots(aSpeed):
    """
    Converts mach to knots.
    """

    try:
        if not isinstance(aSpeed, (int, float, decimal.Decimal)):
            return False

        nSpeed = int(round(aSpeed * 661.4708, 0))

    except Exception:
        myLogger.exception(
            "Exception in [file: %s | module: %s | line: %s]: %s",
            os.path.basename(traceback.extract_stack()[-1][0]),
            traceback.extract_stack()[-1][2],
            traceback.extract_stack()[-1][1],
            sys.exc_info()[1],
        )
        return None

    return nSpeed


def getOperators():
    """
    Get operators
    """

    lOperators = {}

    try:
        with open(Config.operatorsJSON, "r") as oFH:
            operatorData = json.loads(oFH.read())

        for sKey, sValue in operatorData.items():
            if sValue["n"] and sValue["c"] and sValue["r"]:
                lOperators[sKey] = (sValue["n"], sValue["c"], sValue["r"])

    except Exception:
        myLogger.exception(
            "Exception in [file: %s | module: %s | line: %s]: %s",
            os.path.basename(traceback.extract_stack()[-1][0]),
            traceback.extract_stack()[-1][2],
            traceback.extract_stack()[-1][1],
            sys.exc_info()[1],
        )
        return None

    return lOperators


def getAircrafts():
    """
    Get aircrafts
    """

    lAircrafts = {}

    try:
        with open(Config.aircraftsJSON, "r") as aFH:
            aircraftsData = json.loads(aFH.read())

        for sKey, sValue in aircraftsData.items():
            if sValue["f"] and sValue["d"]:
                lAircrafts[sKey] = (sValue["f"], sValue["d"])

    except Exception:
        myLogger.exception(
            "Exception in [file: %s | module: %s | line: %s]: %s",
            os.path.basename(traceback.extract_stack()[-1][0]),
            traceback.extract_stack()[-1][2],
            traceback.extract_stack()[-1][1],
            sys.exc_info()[1],
        )
        return None

    return lAircrafts


def loadFlightData():
    """
    Load data json
    """

    try:
        flightData = json.loads(urlopen(Config.DATA).read().decode())

    except Exception:
        myLogger.exception(
            "Exception in [file: %s | module: %s | line: %s]: %s",
            os.path.basename(traceback.extract_stack()[-1][0]),
            traceback.extract_stack()[-1][2],
            traceback.extract_stack()[-1][1],
            sys.exc_info()[1],
        )
        return None

    return flightData


def getEmoji(aCountry):
    """
    Get country emoji
    """

    bEmoji = ""

    try:
        if aCountry in Config.dCountryCodes:
            bEmoji = flag.flagize(":%s:" % (Config.dCountryCodes[aCountry]))

    except Exception:
        myLogger.exception(
            "Exception in [file: %s | module: %s | line: %s]: %s",
            os.path.basename(traceback.extract_stack()[-1][0]),
            traceback.extract_stack()[-1][2],
            traceback.extract_stack()[-1][1],
            sys.exc_info()[1],
        )
        return None

    return bEmoji


def openBrowser():
    """
    Open browser
    """

    try:
        chromeOptions = SO()
        chromeOptions.add_argument("--headless")
        chromeOptions.add_argument("--hide-scrollbars")
        chromeOptions.add_argument("window-size=%s" % (Config.bWindowSize))

        sBrowser = webdriver.Chrome(
            executable_path=Config.chromeDriver, chrome_options=chromeOptions
        )
        sBrowser.set_page_load_timeout(Config.requestTimeout)

        myLogger.debug("Opening [%s]", Config.URL)
        sBrowser.get(Config.URL)

        try:
            time.sleep(Config.sleepTime)
            sElement = SW(sBrowser, Config.requestTimeout).until(
                SC.element_to_be_clickable((BY.ID, "dump1090_version"))
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

        # Settings Cog
        settingsCog = sBrowser.find_element_by_class_name("settingsContainer")
        settingsCog.click()
        
        # Dim Map
        dimMap = sBrowser.find_element_by_id("MapDim_cb")
        dimMap.click()

        # Altitude Chart
        altitudeChart = sBrowser.find_element_by_id("altitudeChart_cb")
        altitudeChart.click()
        
        # Close Settings
        settingsCloseBox = sBrowser.find_element_by_class_name("settingsCloseBox")
        settingsCloseBox.click()

        # Move cursor
        sActions = AC(sBrowser)
        sActions.move_to_element(sElement).perform()

    except Exception:
        myLogger.exception(
            "Exception in [file: %s | module: %s | line: %s]: %s",
            os.path.basename(traceback.extract_stack()[-1][0]),
            traceback.extract_stack()[-1][2],
            traceback.extract_stack()[-1][1],
            sys.exc_info()[1],
        )
        return None

    return sBrowser


def getScreenshot(sBrowser, aFlight):
    """
    Get Screenshot and crop it
    """

    bScreenshot = False

    try:
        clickPlane = sBrowser.find_elements_by_xpath("//td[text()='%s']" % aFlight.upper())

        if clickPlane:
            if len(clickPlane) >= 1:
                clickPlane = clickPlane[0]

            clickPlane.click()

            # Hide sidebar
            hideSidebar = sBrowser.find_element_by_class_name("hide_sidebar")
            hideSidebar.click()

            time.sleep(Config.sleepTime)

            bScreenshot = sBrowser.get_screenshot_as_png()
            bScreenshot = Image.open(BytesIO(bScreenshot))
            bScreenshot = bScreenshot.crop(
                (Config.cropX, Config.cropY, Config.cropWidth, Config.cropHeight)
            )
            bScreenshot.save("%s.png" % (aFlight))

            # Show sidebar
            showSidebar = sBrowser.find_element_by_class_name("show_sidebar")
            showSidebar.click()

        else:
            myLogger.exception("Cannot click on [%s]", aFlight)
            return None

    except Exception:
        myLogger.exception(
            "Exception in [file: %s | module: %s | line: %s]: %s",
            os.path.basename(traceback.extract_stack()[-1][0]),
            traceback.extract_stack()[-1][2],
            traceback.extract_stack()[-1][1],
            sys.exc_info()[1],
        )
        return None

    return bScreenshot


def formStatus(aCraft, tFlights, pTime):
    """
    Form Tweet Status
    """

    sStatus = ""

    try:
        if aCraft.aCountry:
            sStatus += "%s" % (getEmoji(aCraft.aCountry))

        if aCraft.aCallsign:
            sStatus += " %s" % (aCraft.aCallsign)

        if aCraft.aFlight:
            sStatus += " #%s" % (aCraft.aFlight)
        else:
            myLogger.debug("Cannot find flight information for [%s]", aCraft.aHex)
            sStatus += " #%s" % (aCraft.aHex)

        sStatus += ": %smi away [%s%s elevation]" % (
            aCraft.aDistance,
            aCraft.aElevation,
            u"\N{DEGREE SIGN}",
        )

        if aCraft.aAltitude:
            sStatus += " @ %sft" % (aCraft.aAltitude)

        if aCraft.aHeading:
            sStatus += ", heading %s" % (aCraft.aHeading)

        if aCraft.aSpeed:
            sStatus += " @ %smph" % (aCraft.aSpeed)

        if aCraft.aOperator and aCraft.aType:
            sStatus += " [%s - #%s]" % (aCraft.aOperator, aCraft.aType)
        elif aCraft.aOperator and not aCraft.aType:
            sStatus += " [%s]" % (aCraft.aOperator)
        elif not aCraft.aOperator and aCraft.aType:
            sStatus += " [#%s]" % (aCraft.aType)

        if aCraft.aFlags:
            if aCraft.aFlags == "01":
                myLogger.debug(
                    "Interesting flight (Flag 01) [%s|%s]!",
                    aCraft.aHex,
                    aCraft.aFlight,
                )
                sStatus += " #Interesting"
            elif aCraft.aFlags == "10":
                myLogger.debug(
                    "Military flight (Flag 10) [%s|%s]!",
                    aCraft.aHex,
                    aCraft.aFlight,
                )
                sStatus += " #Military"
            elif aCraft.aFlags == "11":
                myLogger.debug(
                    "Military/Interesting flight (Flag 11) [%s|%s]!",
                    aCraft.aHex,
                    aCraft.aFlight,
                )
                sStatus += " #Military/Interesting"

        if aCraft.aSquawk:
            if aCraft.aSquawk == "7500":
                myLogger.debug(
                    "Hijack (Squawk 7500) [%s|%s]!",
                    aCraft.aHex,
                    aCraft.aFlight,
                )
                sStatus += " #AircraftHijacking #Squawk7500"
            elif aCraft.aSquawk == "7600":
                myLogger.debug(
                    "Radio Failure (Squawk 7600) [%s|%s]!",
                    aCraft.aHex,
                    aCraft.aFlight,
                )
                sStatus += " #RadioFailure #Squawk7600"
            elif aCraft.aSquawk == "7700":
                myLogger.debug(
                    "General Emergency (Squawk 7700) [%s|%s]!",
                    aCraft.aHex,
                    aCraft.aFlight,
                )
                sStatus += " #GeneralEmergency #Squawk7700"

        if aCraft.aEmergency:
            sStatus += " #%s" % (aCraft.aEmergency)

        sStatus += Config.defaultHashtags
        sStatus += " [Total Flights: %s]" % (tFlights)
        sStatus += " @ [%s]" % (pTime)

    except Exception:
        myLogger.exception(
            "Exception in [file: %s | module: %s | line: %s]: %s",
            os.path.basename(traceback.extract_stack()[-1][0]),
            traceback.extract_stack()[-1][2],
            traceback.extract_stack()[-1][1],
            sys.exc_info()[1],
        )
        return None

    return sStatus


def tweetNow(bImage, sStatus):
    """
    Tweet now
    """

    bMedia = False
    nRetryCount = 0

    try:
        if bImage:
            bMedia = open(bImage, "rb")
        else:
            myLogger.exception("Cannot open [%s]", bImage)
            return None

        if bMedia:
            tAPI = twython.Twython(
                Config.tConsumerKey,
                Config.tConsumerSecret,
                Config.tAccessToken,
                Config.tAccessTokenSecret,
            )

            sResponse = tAPI.upload_media(media=bMedia)
            tAPI.update_status(status=sStatus, media_ids=[sResponse["media_id"]])
            del tAPI

            myLogger.debug(
                "Flight [%s] tweeted successfully!", os.path.splitext(bImage)[0]
            )
            os.remove(bImage)

    except Exception:
        myLogger.exception(
            "Exception in [file: %s | module: %s | line: %s]: %s",
            os.path.basename(traceback.extract_stack()[-1][0]),
            traceback.extract_stack()[-1][2],
            traceback.extract_stack()[-1][1],
            sys.exc_info()[1],
        )
        return None

    return False
