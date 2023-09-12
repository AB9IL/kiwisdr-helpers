#!/usr/bin/env python3

import datetime
import random
from kiwisdr_stripped import dictlist

# path to the redirect directory
linkpath = '../monitor'
# filter the list of dictionaries by latitude longitude
# use geographic boxes bounded by: (south, north, west, east)
# frequencies(day, night)
# time offset from UTC

# Radio Caroline
UK1_area = ('United Kingdom 1', 48.5, 54.5, -5.5, 7.4, 648, 648, 0, 'sam')

# BBC Radio 4
UK2_area = ('United Kingdom 2', 48.5, 54.5, -5.5, 7.4, 198, 198, 0, 'sam')

regions = (UK1_area, UK2_area)


def make_redirect(dictlist, area):
    lat_range = (area[1], area[2])
    lon_range = (area[3], area[4])
    # first freq is for daytime, second freq for night
    monitor_freqs = (area[5], area[6])
    listcount = 10
    min_snr = 15
    local_hour = area[7] + datetime.datetime.utcnow().hour
    sig_mode = area[8]
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
    output = f'<?php header( "Location: {sdrlist[0]}/?f={local_freq}/-4000,4000{sig_mode}z10&1hz" ) ; ?>'
    yield output


for count, item in enumerate((make_redirect(dictlist, area) for area in regions)):
    item = next(item)
    # write the redirect to the index file
    target_file = f'{linkpath}{count}/index.html'
    with open(target_file, 'w') as file:
        file.write(item)
