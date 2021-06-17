"""
Logger module.
"""

__author__ = "HariA"


import logging
import logging.handlers
import os
import sys
import traceback


sBaseFileName = os.path.splitext(os.path.basename(sys.argv[0]))[0]
sLogFile = "%s.log" % (sBaseFileName)
sLogDir = "/var/log/AircraftTracker"


def setLogger():
    """
    Set the logger
    """

    try:
        myLogger = logging.getLogger(sBaseFileName)
        myLogger.setLevel(logging.DEBUG)
        myFormat = logging.Formatter(
            "%(asctime)s [%(levelname)8s] [%(filename)-18s %(lineno)3d] %(message)s",
            "%Y-%m-%d %H:%M:%S",
        )

        if not os.path.exists(sLogDir):
            os.makedirs(sLogDir)

        myFileHandler = logging.handlers.RotatingFileHandler(
            os.path.join(sLogDir, sLogFile), maxBytes=5 * 1024 * 1024, backupCount=5
        )
        myFileHandler.setLevel(logging.DEBUG)
        myFileHandler.setFormatter(myFormat)
        myLogger.addHandler(myFileHandler)

        myStreamHandler = logging.StreamHandler()
        myStreamHandler.setLevel(logging.INFO)
        # myStreamHandler.setFormatter(myFormat)
        myLogger.addHandler(myStreamHandler)

    except Exception:
        print(
            "Exception in [file: %s | module: %s | line: %s]: %s",
            os.path.basename(traceback.extract_stack()[-1][0]),
            traceback.extract_stack()[-1][2],
            traceback.extract_stack()[-1][1],
            sys.exc_info()[1],
            extra={"mhz": "[%s]" % sKey},
        )
        raise

    return myLogger
