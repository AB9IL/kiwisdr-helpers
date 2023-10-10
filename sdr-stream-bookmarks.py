#!/usr/bin/env python3

import datetime
import random
from kiwisdr_stripped import dictlist

source_file = '/usr/local/src/kiwidata/sdr-stream-bookmarks-template'
target_file = '/usr/local/src/kiwidata/sdr-stream-bookmarks'

# filter the list of dictionaries by latitude longitude
# use geographic boxes bounded by: (south, north, west, east)
# frequencies(day, night)
# time offset from UTC

# Newfoundland
Newfoundland = ('Newfoundland', 45.0, 52.0, -66.5, -52.0, 5000, 10000, -5)
# Montreal
Montreal = ('Montreal', 44.5, 47.0, -75.5, -72.0, 5000, 10000, -5)
# Ottawa
Ottawa = ('Ottawa', 44.5, 46.5, -77.0, -74.0, 5000, 10000, -5)
# Oshawa
Oshawa = ('Oshawa', 43.0, 44.5, -81.0, -77.5, 5000, 10000, -5)
# Winnipeg
Winnipeg = ('Winnipeg', 49.0, 51.0, -98.5, -95.5, 5000, 10000, -6)
# Watrous
Watrous = ('Watrous', 50.3, 54.0, -112.0, -103.5, 5000, 10000, -6)
# Edmonton
Edmonton = ('Edmonton', 51.0, 56.0, -117.0, -110.0, 5000, 10000, -7)
# Vancouver
Vancouver = ('Vancouver', 48.0, 50.2, -126.0, -119.0, 5000, 10000, -8)
# New York
New_York = ('New York', 39.7, 42.0, -76.4, -72.0, 5000, 10000, -5)
# Wisconsin
Wisconsin = ('Wisconsin', 41.0, 47.3, -93.8, -86.6, 5000, 10000, -6)
# Chicago
Chicago = ('Chicago', 39.5, 42.5, -90.0, -86.0, 5000, 10000, -6)
# Shannon (IE)
Shannon = ('Shannon', 51.2, 54.5, -10.7, -7.4, 5000, 10000, 0)
# Dublin (IE)
Dublin = ('Dublin', 52.3, 55.0, -9.0, -3.0, 5000, 10000, 0)
# Denmark Area
Denmark_Area = ('Denmark Area', 52.5, 60.5, -3.0, 20.0, 5000, 10000, 1)
# London (UK)
London_UK = ('London (UK)', 49.8, 53.5, -5.4, 3.4, 5000, 10000, 0)
# France_Belgium
France_Belgium = ('France & Belgium', 42.0, 52.0, -5.0, 10.0, 5000, 10000, 0)
# NewSouthWales (AUS)
NewSouthWales_AUS = ('NewSouthWales (AUS)', -35.5, -32.5, 148.8, 152, 5000, 10000, 0)
# South East Asia
South_East_Asia = ('South East Asia', -11.0, 18.7, 92.0, 127.0, 5000, 10000, 7)
# Midwest (US)
Midwest_US = ('Midwest (US)', 37.0, 43.5, -91.5, -80.0, 5000, 10000, -5)
# Pennsylvania
Pennsylvania = ('Pennsylvania', 39.7, 42.0, -84.5, -74.5, 5000, 10000, -4)
# Arkansas
Arkansas = ('Arkansas', 31.0, 39.0, -98.0, -86.0, 5000, 10000, -5)
# Utah_Arizona
Utah_Arizona = ('Utah_Arizona', 33.3, 42.0, -114.0, -109.0, 5000, 10000, -7)
# San Francisco
San_Francisco = ('San Francisco', 37.0, 39.0, -123.0, -120.0, 5000, 10000, -7)
# Southeast (US)
Southeast_US = ('Southeast_US', 24.0, 36.5, -91.5, -74.5, 5000, 10000, -4)
# NAT Tracks West
NAT_West_area = ('NAT West', 40.2, 47.2, -76.9, -52.0, 5000, 10000, -4)
# WATRS
WATRS_area = ('WATRS', 17.0, 42.0, -84.0, -62.0, 5000, 10000, -4)
# CEPAC
CEPAC_area = ('CEPAC', 16.0, 52.0, -163.0, -116.0, 5000, 10000, -9)
# HFGCS Northeast
HFGCS_NE = ('HFGCS Northeast', 40.9, 46.0, -75.0, -69.0, 5000, 10000, -4)
# HFGCS Northwest
HFGCS_NW = ('HFGCS Northwest', 38.7, 51.7, -126.0, -103.5, 5000, 10000, -7)

regions = (Newfoundland, Montreal, Ottawa, Oshawa, Winnipeg, Watrous, Edmonton,
           Vancouver, New_York, Wisconsin, Chicago, Shannon, Dublin, Denmark_Area,
           London_UK, France_Belgium, NewSouthWales_AUS, South_East_Asia, Midwest_US,
           Pennsylvania, Arkansas, Utah_Arizona, Southeast_US, NAT_West_area,
           WATRS_area, CEPAC_area, HFGCS_NE, HFGCS_NW)

def make_link(dictlist, area):
    lat_range = (area[1], area[2])
    lon_range = (area[3], area[4])
    # first freq is for daytime, second freq for night
    monitor_freqs = (area[5], area[6])
    listcount = 10
    min_snr = 8
    local_hour = area[7] + datetime.datetime.utcnow().hour
    # select day or night frequency
    local_freq = area[6]
    if local_hour >= 7 and local_hour < 18:
        local_freq = area[5]
    dictlist = list(filter(lambda site: int(site["snr"][-2:].replace(',', ''))
                    > min_snr, dictlist))
    # sort the list of dicts by snr
    dictlist.sort(key=lambda item: item.get("snr"), reverse=True)
    dictlist = list(filter(lambda site: float(site["gps"].split(',')[0][1:])
                    > lat_range[0], dictlist))
    dictlist = list(filter(lambda site: float(site["gps"].split(',')[0][1:])
                    < lat_range[1], dictlist))
    dictlist = list(filter(lambda site: float(site["gps"].split(',')[1][:-1])
                    > lon_range[0], dictlist))
    dictlist = list(filter(lambda site: float(site["gps"].split(',')[1][:-1])
                    < lon_range[1], dictlist))
    # exclude sites with no available channels
    dictlist = list(filter(lambda site: float(site["users"])
                    < float(site["users_max"]), dictlist))
    # truncate the list
    dictlist = dictlist[0:listcount]
    # build the list of servers
    sdrlist = [entry.get('url') for entry in dictlist]
    random.shuffle(sdrlist)
    # For the bookmarks, we want only the SDR URL
    try:
        output = (area, sdrlist[0])
    except Exception:
        output = (area, "127.0.0.1")
        pass
    yield output

with open(source_file, 'r') as file:
    oldstuff = file.read()

# open the template and read the data
# the generator should return one URL for each area
# replace strings: area for URL
for item in (make_link(dictlist, area) for area in regions):
    item = next(item)
    # substitute a URL for area placeholder
    string1 = f'"{item[0][0]}'
    string2 = f'"{item[1]}/'
    oldstuff = oldstuff.replace(string1, string2)

with open(target_file, 'w') as file:
    file.write(oldstuff)

