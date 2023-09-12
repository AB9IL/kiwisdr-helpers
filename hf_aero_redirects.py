#!/usr/bin/env python3

import datetime
import random
from kiwisdr_stripped import dictlist

# filter the list of dictionaries by latitude longitude
# use geographic boxes bounded by: (south, north, west, east)
# frequencies(day, night)
# time offset from UTC

# NAT Tracks West
NAT_West_area = ('NAT West', 40.2, 47.2, -76.9, -52.0, 8906, 5598, -4)

# NAT Tracks East
NAT_East_area = ('NAT East', 48.8, 59.0, -11.5, 7.0, 8864, 5616, -1)

# Atlantic West
Atlantic_West_area = ('Atlantic West', 17.0, 48.0, -80.0, -61.5, 8825, 6628, -4)

# Atlantic East
Atlantic_East_area = ('Atlantic East', 13.0, 59.0, -28.0, 7.0, 11396, 8906, -1)

# WATRS
WATRS_area = ('WATRS', 17.0, 42.0, -84.0, -62.0, 8846, 6577, -4)

# South Atlantic 1
SAT1_area = ('South Atlantic 1', -29.0, 20.0, -57.0, 19.0, 13357, 8861, -2)

# CEPAC
CEPAC_area = ('CEPAC', 16.0, 52.0, -163.0, -116.0, 8843, 5574, -9)

# NOPAC East
NOPAC_East_area = ('NOPAC East', 17.0, 65.0, -170.0, -119.0, 8951, 6655, -9)

# NOPAC West
NOPAC_West_area = ('NOPAC West', 20.0, 57.0, 24.5, 170.0, 8951, 6655, 9)

# CWPAC
CWP1_area = ('CWPAC', 5.0, 48.0, 112.5, 148.0, 8903, 6532, 11)

# South East Asia 2
SEA2_area = ('South East Asia 2', -11.5, 26.0, 92.0, 142.0, 8942, 5655, 8)

# South East Asia 3
SEA3_area = ('South East Asia 3', -28.0, 23.5, 96.0, 175.0, 11396, 6556, 7)

# South Pacific
SOPAC_area = ('South Pacific', -50.0, 5.0, 135.0, 179.9, 8867, 5643, 11)

regions = (NAT_West_area, NAT_East_area, Atlantic_West_area, Atlantic_East_area,
           WATRS_area, SAT1_area, CEPAC_area, NOPAC_East_area, NOPAC_West_area,
           CWP1_area, SEA2_area, SEA3_area, SOPAC_area)


def make_redirect(dictlist, area):
    lat_range = (area[1], area[2])
    lon_range = (area[3], area[4])
    # first freq is for daytime, second freq for night
    monitor_freqs = (area[5], area[6])
    listcount = 10
    min_snr = 15
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
    output = f'<?php header( "Location: {sdrlist[0]}/?f={local_freq}/100,3000usbz10&1hz" ) ; ?>'
    yield output

for count, item in enumerate((make_redirect(dictlist, area) for area in regions)):
    item = next(item)
    # write the redirect to the index file
    target_file = f'../hf-aero{count}/index.html'
    with open(target_file, 'w') as file:
        file.write(item)
