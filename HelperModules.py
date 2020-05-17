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

        directionList = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]

        sValue = int(math.floor((headingTrack / 22.5) + 0.5))
        sDirection = directionList[(sValue % 16)]

    except Exception:
        myLogger.exception("Exception in [file: %s | module: %s | line: %s]: %s", os.path.basename(traceback.extract_stack()[-1][0]), traceback.extract_stack()[-1][2], traceback.extract_stack()[-1][1], sys.exc_info()[1], extra={"MHz": ""})
        return False

    return sDirection


def distanceFromAtoB(pA, pB):
    """
    Calculate the great circle distance between two points on the earth (specified in decimal degrees)

    http://stackoverflow.com/questions/15736995/how-can-i-quickly-estimate-the-distance-between-two-latitude-longitude-points
    """

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

        latitudeOne, longitudeOne, latitudeTwo, longitudeTwo = map(math.radians, [pA[0], pA[1], pB[0], pB[1]])

        dLatitude = latitudeTwo - latitudeOne
        dLongitude = longitudeTwo - longitudeOne

        a = math.sin(dLatitude / 2) ** 2 + math.cos(latitudeOne) * math.cos(latitudeTwo) * math.sin(dLongitude / 2) ** 2
        c = 2 * math.asin(math.sqrt(a))

        nDistance = round(3956 * c, 2)

    except Exception:
        myLogger.exception("Exception in [file: %s | module: %s | line: %s]: %s", os.path.basename(traceback.extract_stack()[-1][0]), traceback.extract_stack()[-1][2], traceback.extract_stack()[-1][1], sys.exc_info()[1], extra={"MHz": ""})
        return False

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

        nElevation = round(math.degrees(math.atan(aAltitude / (aDistance * 5280))), 2)

    except Exception:
        myLogger.exception("Exception in [file: %s | module: %s | line: %s]: %s", os.path.basename(traceback.extract_stack()[-1][0]), traceback.extract_stack()[-1][2], traceback.extract_stack()[-1][1], sys.exc_info()[1], extra={"MHz": ""})
        return False

    return nElevation


def knots2mph(aSpeed):
    """
    Converts knots to mph.
    """

    try:
        if not isinstance(aSpeed, (int, float, decimal.Decimal)):
            return False

        nSpeed = round(aSpeed * 1.15078, 2)

    except Exception:
        myLogger.exception("Exception in [file: %s | module: %s | line: %s]: %s", os.path.basename(traceback.extract_stack()[-1][0]), traceback.extract_stack()[-1][2], traceback.extract_stack()[-1][1], sys.exc_info()[1], extra={"MHz": ""})
        return False

    return nSpeed


def mach2knots(aSpeed):
    """
    Converts mach to knots.
    """

    try:
        if not isinstance(aSpeed, (int, float, decimal.Decimal)):
            return False

        nSpeed = round(aSpeed * 661.4708, 2)

    except Exception:
        myLogger.exception("Exception in [file: %s | module: %s | line: %s]: %s", os.path.basename(traceback.extract_stack()[-1][0]), traceback.extract_stack()[-1][2], traceback.extract_stack()[-1][1], sys.exc_info()[1], extra={"MHz": ""})
        return False

    return nSpeed


def getOperators():
    """
    Get operators
    """

    lOperators = {}

    try:
        with open(Config.operatorsJSON) as oFH:
            operatorData = json.loads(oFH.read())

        for sKey, sValue in operatorData.items():
            if sValue["n"] and sValue["c"] and sValue["r"]:
                lOperators[sKey] = (sValue["n"], sValue["c"], sValue["r"])

    except Exception:
        myLogger.exception("Exception in [file: %s | module: %s | line: %s]: %s", os.path.basename(traceback.extract_stack()[-1][0]), traceback.extract_stack()[-1][2], traceback.extract_stack()[-1][1], sys.exc_info()[1], extra={"MHz": ""})
        return False

    return lOperators


def getAircrafts():
    """
    Get aircrafts
    """

    lAircrafts = {}

    try:
        with open(Config.aircraftsJSON) as aFH:
            aircraftsData = json.loads(aFH.read())

        for sKey, sValue in aircraftsData.items():
            if sValue["f"] and sValue["d"]:
                lAircrafts[sKey] = (sValue["f"], sValue["d"])

    except Exception:
        myLogger.exception("Exception in [file: %s | module: %s | line: %s]: %s", os.path.basename(traceback.extract_stack()[-1][0]), traceback.extract_stack()[-1][2], traceback.extract_stack()[-1][1], sys.exc_info()[1], extra={"MHz": ""})
        return False

    return lAircrafts


def loadFlightData(sKey, dataURL):
    """
    Load data json
    """

    try:
        flightData = json.loads(urlopen(dataURL).read().decode())

    except Exception:
        myLogger.exception("Exception in [file: %s | module: %s | line: %s]: %s", os.path.basename(traceback.extract_stack()[-1][0]), traceback.extract_stack()[-1][2], traceback.extract_stack()[-1][1], sys.exc_info()[1], extra={"MHz": ""})
        return False

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
        myLogger.exception("Exception in [file: %s | module: %s | line: %s]: %s", os.path.basename(traceback.extract_stack()[-1][0]), traceback.extract_stack()[-1][2], traceback.extract_stack()[-1][1], sys.exc_info()[1], extra={"MHz": ""})
        return False

    return bEmoji


def openBrowser(sKey, mapURL, zoom):
    """
    Open browser
    """

    try:
        chromeOptions = SO()
        chromeOptions.add_argument("headless")
        chromeOptions.add_argument("window-size=%s" % (Config.bWindowSize))
        sBrowser = webdriver.Chrome(executable_path=Config.chromeDriver, chrome_options=chromeOptions)
        sBrowser.set_page_load_timeout(Config.requestTimeout)

        myLogger.debug("Opening [%s]", mapURL, extra={"MHz": "[%s]" % sKey})
        sBrowser.get(mapURL)

        try:
            sElement = SW(sBrowser, Config.requestTimeout).until(SC.element_to_be_clickable((BY.ID, "dump1090_version")))

        except SE.TimeoutException:
            myLogger.exception("Exception in [file: %s | module: %s | line: %s]: %s", os.path.basename(traceback.extract_stack()[-1][0]), traceback.extract_stack()[-1][2], traceback.extract_stack()[-1][1], sys.exc_info()[1], extra={"MHz": "[%s]" % sKey})
            return False

        myLogger.debug("Zoom in [%s] times", zoom, extra={"MHz": "[%s]" % sKey})
        try:
            zoomIn = sBrowser.find_element_by_class_name("ol-zoom-in")

        except SE.NoSuchElementException:
            zoomIn = sBrowser.find_elements_by_xpath('//*[@title="Zoom in"]')
            if zoomIn:
                zoomIn = zoomIn[0]

        for i in range(zoom):
            zoomIn.click()
            time.sleep(i)

    except Exception:
        myLogger.exception("Exception in [file: %s | module: %s | line: %s]: %s", os.path.basename(traceback.extract_stack()[-1][0]), traceback.extract_stack()[-1][2], traceback.extract_stack()[-1][1], sys.exc_info()[1], extra={"MHz": "[%s]" % sKey})
        return False

    return sBrowser


def getScreenshot(sKey, sBrowser, aHex):
    """
    Get Screenshot and crop it
    """

    bScreenshot = False

    try:
        clickPlane = sBrowser.find_elements_by_xpath("//td[text()='%s']" % aHex.lower())

        if clickPlane:
            myLogger.debug("Clicking on [%s]!", aHex, extra={"MHz": "[%s]" % sKey})
            if len(clickPlane) >= 1:
                clickPlane = clickPlane[0]

            clickPlane.click()
            time.sleep(Config.sleepTime)

            myLogger.debug("Hide Sidebar", extra={"MHz": "[%s]" % sKey})
            try:
                hideSidebar = sBrowser.find_element_by_class_name("hide_sidebar")

            except SE.NoSuchElementException:
                hideSidebar = sBrowser.find_elements_by_xpath('//*[@title="Toggle Sidebar"]')
                if hideSidebar:
                    hideSidebar = hideSidebar[0]

            hideSidebar.click()

        else:
            myLogger.debug("Cannot click on [%s]", aHex, extra={"MHz": "[%s]" % sKey})
            return False

        myLogger.debug("Taking screenshot", extra={"MHz": "[%s]" % sKey})
        bScreenshot = sBrowser.get_screenshot_as_png()
        bScreenshot = Image.open(BytesIO(bScreenshot))
        bScreenshot = bScreenshot.crop((Config.cropX, Config.cropY, Config.cropWidth, Config.cropHeight))
        bScreenshot.save("%s.png" % (aHex))

        myLogger.debug("Show Sidebar", extra={"MHz": "[%s]" % sKey})
        try:
            showSidebar = sBrowser.find_element_by_class_name("show_sidebar")

        except SE.NoSuchElementException:
            showSidebar = sBrowser.find_elements_by_xpath('//*[@title="Toggle Sidebar"]')
            if showSidebar:
                showSidebar = showSidebar[0]

        showSidebar.click()

    except Exception:
        myLogger.exception("Exception in [file: %s | module: %s | line: %s]: %s", os.path.basename(traceback.extract_stack()[-1][0]), traceback.extract_stack()[-1][2], traceback.extract_stack()[-1][1], sys.exc_info()[1], extra={"MHz": "[%s]" % sKey})
        return False

    return bScreenshot


def formStatus(sKey, aCraft, pTime):
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
            myLogger.debug("Cannot find flight information for [%s]", aCraft.aHex, extra={"MHz": "[%s]" % sKey})
            sStatus += " #%s" % (aCraft.aHex)

        if aCraft.aDistance < Config.distanceAlarm:
            sStatus += ": %sm away @" % (aCraft.aDistance)
        else:
            sStatus += ": %s%s elevation @" % (aCraft.aElevation, u"\N{DEGREE SIGN}")

        if aCraft.aAltitude:
            sStatus += " %sft," % (aCraft.aAltitude)

        if aCraft.aHeading:
            sStatus += " heading %s @" % (aCraft.aHeading)

        if aCraft.aSpeed:
            sStatus += " %smph" % (aCraft.aSpeed)

        if aCraft.aOperator and aCraft.aType:
            sStatus += " [%s - #%s]" % (aCraft.aOperator, aCraft.aType)
        elif aCraft.aOperator and not aCraft.aType:
            sStatus += " [%s]" % (aCraft.aOperator)
        elif not aCraft.aOperator and aCraft.aType:
            sStatus += " [#%s]" % (aCraft.aType)

        if aCraft.aFlags:
            if aCraft.aFlags == "01":
                sStatus += " #Interesting"
            elif aCraft.aFlags == "10":
                sStatus += " #Military"
            elif aCraft.aFlags == "11":
                sStatus += " #Military/Interesting"

        if aCraft.aSquawk:
            if aCraft.aSquawk == "7500":
                sStatus += " #AircraftHijacking"
            elif aCraft.aSquawk == "7600":
                sStatus += " #RadioFailure"
            elif aCraft.aSquawk == "7700":
                sStatus += " #GeneralEmergency"

        if aCraft.aEmergency:
            sStatus += " #%s" % (aCraft.aEmergency)

        sStatus += Config.defaultHashtags % (sKey.strip())
        sStatus += " [%s]" % (pTime)

    except Exception:
        myLogger.exception("Exception in [file: %s | module: %s | line: %s]: %s", os.path.basename(traceback.extract_stack()[-1][0]), traceback.extract_stack()[-1][2], traceback.extract_stack()[-1][1], sys.exc_info()[1], extra={"MHz": "[%s]" % sKey})
        return False

    return sStatus


def tweetNow(sKey, bImage, sStatus):
    """
    Tweet now
    """

    bMedia = False
    nRetryCount = 0

    try:
        if bImage:
            bMedia = open(bImage, "rb")
        else:
            myLogger.exception("Cannot open [%s]", bImage, extra={"MHz": "[%s]" % sKey})
            return False

        if bMedia:
           tAPI = twython.Twython(Config.tConsumerKey, Config.tConsumerSecret, Config.tAccessToken, Config.tAccessTokenSecret)

           sResponse = tAPI.upload_media(media=bMedia)
           tAPI.update_status(status=sStatus, media_ids=[sResponse["media_id"]])
           del tAPI

           myLogger.debug("Tweeted successfully! Deleting [%s]", bImage, extra={"MHz": "[%s]" % sKey})
           os.remove(bImage)

    except Exception:
        myLogger.exception("Exception in [file: %s | module: %s | line: %s]: %s", os.path.basename(traceback.extract_stack()[-1][0]), traceback.extract_stack()[-1][2], traceback.extract_stack()[-1][1], sys.exc_info()[1], extra={"MHz": "[%s]" % sKey})
        return False

    return False

