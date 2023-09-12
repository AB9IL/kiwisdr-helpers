#!/usr/bin/env python3

import shutil
from kiwisdr_stripped import dictlist

# file for inclusion in html
origin_txt_file = "../kiwisdr-canada.html.orig"
final_txt_file = "../kiwisdr-canada.html"
shutil.copy(origin_txt_file, final_txt_file)

# filter the list of dictionaries by latitude longitude
# use geographic boxes bounded by: (south, north, west, east)
# Halifax, NS
halifax_area = ['--Halifax--', 43.0, 49.0, -67.5, -57.5]

# Montreal, QC
montreal_area = ['--Montreal--', 44.9, 47.4, -75.0, -72.0]

# Ottawa, QC
ottawa_area = ['--Ottawa--',  44.3, 46.0, -77.0, -74.3]

# Toronto, ON
toronto_area = ['--Toronto--',  42.8, 44.6, -81.3, -77.3]

# Winnipeg, MB
winnipeg_area = ['--Winnipeg--',  49.3, 50.5, -98.5, -96.0]

# Regina and Saskatoon, SK
regsask_area = ['--Regina-Saskatoon--', 47.9, 54.0, -111.9, -98.5]

# Edmonton, AB
edmonton_area = ['--Edmonton--',  51.7, 55.0, -116.0, -110.5]

# Calgary, AB
calgary_area = ['--Calgary--', 49.7, 52.3, -116.0, -111.0]

# Vancouver, BC
vancouver_area = ['--Vancouver--', 48.2, 49.9, -124.0, -120.5]

regions = [halifax_area, montreal_area, ottawa_area, toronto_area, winnipeg_area,
           regsask_area, edmonton_area, calgary_area, vancouver_area]


def sort_servers(dictlist, area):
    global sdrlist
    sdrlist = ''
    lat_range = [area[1], area[2]]
    lon_range = [area[3], area[4]]
    listcount = 5
    min_snr = 9
    dictlist = list(filter(lambda site: int(site["snr"][-2:].replace(',', ''))
                                > min_snr, dictlist))
    # sort the list of dicts by snr, latitude, and longitude
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
    for entry in dictlist:
        site_url = entry.get('url')
        site_location = entry.get('loc')
        output = "  <a href=\"" + site_url + "/?f=${freq}${bp}${sdrmode}z10\" target=\"_blank\">" + "KiwiSDR, " + site_location + "</a></br>\n"
        sdrlist += output
    return sdrlist


# Opening our text file in read only
# mode using the open() function
with open(final_txt_file, 'r') as file:
    data = file.read()

for area in regions:
    # build the column of data
    sort_servers(dictlist, area)
    # close the column
    # text to find for first payload
    search_text = area[0]
    # replacement text
    replace_text = sdrlist
    data = data.replace(search_text, replace_text)

with open(final_txt_file, 'w') as file:
    file.write(data)
