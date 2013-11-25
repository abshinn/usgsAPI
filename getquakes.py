#!/usr/bin/env python3

# PURPOSE
#   Obtain the last six months of earthquake data from USGS, and save to a csv file to be read into R
#   for plotting and analysis.
#
# DEFAULTS
#    start - "startdate" in the USGS query; set to 30 years ago
#      end - "enddate" in the query; set to current time
#   minmag - "minmagnitude" in the query; set to 2.5
#  lat&lon - "latitude" and "longitude" in query; set to 37N 122W (San Francisco)
#   radius - "maxradius" in the query; set to 200km
#
# FURTHER WORK
#   - Adapt to be a generalized interface with the USGS Earthquake API.
#   - Pull down USGS data in JSON format instead of CSV since it provides more information.
#   - Convert main function to be a class to provide scalability.
#
# MODIFICATION
#   - created November 2013 by Adam Shinn

import sys, urllib.request, re, time

parameters = { "starttime": "",
                 "endtime": "",
             "updateafter": "",
           # rectangular box
             "minlatitude": "", 
             "maxlatitude": "",
            "minlongitude": "",
            "maxlongitude": "",
           # circle
                "latitude": "",
               "longitude": "",
               "minradius": "",
             "minradiuskm": "",
               "maxradius": "",
             "maxradiuskm": "",
           # other
                "mindepth": "",
                "maxdepth": "",
            "minmagnitude": "",
            "maxmagnitude": "",
       "includeallorigins": "",
    "includeallmagnitudes": "",
         "includearrivals": "",
           "includedelete": "",
                 "eventid": "",
                   "limit": "",
                  "offset": "",
                 "orderby": "", #time, time-asc, magnitude, magnitude-asc
                 "catalog": "",
             "contributor": "",
           # extensions
                  "format": "", #quakeml, csv, geojson, kml, xml, text
               "eventtype": "", #earthquake will limit non-earthquake events
            "reviewstatus": "",
                  "minmmi": "",
                  "maxmmi": "",
                  "mincdi": "",
                  "maxcdi": "",
                 "minfelt": "",
              "alertlevel": "",
                  "mingap": "",
                  "maxgap": "",
                  "maxsig": "",
             "producttype": ""}

class queryInput(object):
    def __init__(self, start = "", end = "", minmag = ""):
        pass

class usgs(object):
    def __init__(self, **parameters):
        self.parameters = query
            
        except KeyError as msg:
            pass
def getquakes(start = "", end = "today", minmag = "2.5", lat = "37", lon = "-122", radius = "200"):
    """Queries USGS API and saves result to csv file."""

    # start time
    if not start:
        # calculate time, default is today - 30 years
        # note: time.time() provides unix time, which is in seconds past the 1970 epoch
        #sixmonths = 3600*24*30*6 # [seconds]
        thirtyyears = 3600*24*365*30 # [seconds]
        start = time.strftime("%Y-%m-%d+%H:%M:%S", time.gmtime(time.time() - thirtyyears))
        start = re.sub(r":", r"%3A", start) # replace colon with appropriate html code

    # end time
    if end == "today":
        end = time.strftime("%Y-%m-%d+%H:%M:%S", time.gmtime())

    # USGS API Query
    # The documentation for this API can be found at:
    #   http://comcat.cr.usgs.gov/fdsnws/event/1/
    url = "http://comcat.cr.usgs.gov/fdsnws/event/1/query?" \
          "starttime={}&endtime={}&minmagnitude={}&latitude={}&" \
          "longitude={}&minradiuskm=0&maxradiuskm={}&format=csv".format(start, end, minmag, lat, lon, radius)

    print("Querying USGS with: {}".format(url))
    with urllib.request.urlopen(url) as usgs:
        response = usgs.read()

    #try:
    #    response = urllib2.urlopen(url)
    #except urllib2.URLError as msg:
    #    print("Failed to reach url.\nReason: {}".format(msg))
    #    sys.exit()

    # write the url response to a csv file
    filename = "quake_last3decades.csv"
    print("Writing results to: {}".format(filename))
    with open(filename, "w") as csv:
        csv.write(response)

    # close urllib2 file object
    #response.close()

if __name__ == '__main__':
    getquakes()

