# AboveBracknell

[AboveBracknell](https://twitter.com/abovebracknell) is an ADS-B Twitter Bot running on a Raspberry Pi.
It tracks airplanes and then tweets whenever an airplane flies overhead.

 * Uses [tar1090](https://github.com/wiedehopf/tar1090) for ADSB message decoding, airplane tracking, and webserving.
 * It tweets an image of a map with the airplane's track.
 * It displays the flight name if available, or the reported ICAO code.
 * It displays altitude, ground speed and heading information of the airplane at it's closest point to the bot.
 * It displays the airline name and the aircraft manufacturer and type

The Raspberry Pi must already be running ADS-B decoding software. Many prebuilt images of these exist.
Preferred Option:
 * [ADSB Exchange](https://www.adsbexchange.com/how-to-feed/adsbx-custom-pi-image/)
Other Options:
 * [PiAware by FlightAware](https://uk.flightaware.com/adsb/piaware/build)
 * [FlightRadar24](https://www.flightradar24.com/build-your-own)

## Example Tweets
![](https://i.imgur.com/FFYagYP.png)
![](https://i.imgur.com/xHPaVKw.png)
![](https://i.imgur.com/bcsInS8.png)

## Hardware

 * RaspberryPi - 4B recommended (2B and 3B will work)
 * 16GB minimum MicroSD card
 * RTL-SDR dongle (FlightAware Pro Stick Plus) - generic RTL-SDR dongles will work
 * 1090MHz antenna (FlightAware ADS-B antenna) - home-made "cantenna"s will also work

## Dependencies
* python3
* Tar1090 (For ADSB decoding)
* Pillow, Chromedriver and Selenium (To create screenshots)
* Twython (to tweet messages)

Also Requires:
* aircrafts.json
* operators.json

Both can be found at [Micrtronics.de](http://www.mictronics.de/) under Aircraft Database. Use the Export function on the website

## Install Instructions:
* Clone the repository to the Pi
* Edit the Config.py file - add Twitter keys and change Lat/Lon as required
* Transfer the aircrafts.json and operators.json files to the AboveBracknell folder.
* Install Pillow, Selenum and Twython using pip3
* Install chromium-chromedriver using apt
* modify Tar1090 /usr/local/share/tar1090/html/config.js file to set ICAO code to be shown by default (screenshot fails without this change)
* run the runAircraftTracker.sh script file

## Modified from
* [ha7777](https://github.com/ha7777)

## Contributors
* [Kevin Brandon](https://github.com/kevinabrandon)
* [Joseph Prochazka](https://github.com/jprochazka)
* [ha7777](https://github.com/ha7777)


