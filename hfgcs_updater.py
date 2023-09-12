#!/usr/bin/env python3

import shutil
from kiwisdr_stripped import dictlist

# file for inclusion in html
origin_txt_file = "../hfgcs-quick-tune-list.html.orig"
final_txt_file = "../hfgcs-quick-tune-list.html"
shutil.copy(origin_txt_file, final_txt_file)

# filter the list of dictionaries by latitude longitude
# use geographic boxes bounded by: (south, north, west, east)
# New England
neweng_area = ['New England', 40.9, 46.0, -75.0, -69.0]

# Pacific Northwest
pacnw_area = ['Pacific Northwest', 38.7, 51.7, -126.0, -103.5]

# Hawaii
hawaii_area = ['Hawaii', 18.0, 23.0, -161.0, -154.0]

# Western Europe
westeurope_area = ['Western Europe', 49.0, 54.0, 1.0, 14.5]

# Southern Europe
southeurope_area = ['Southern Europe', 36.0, 44.0, 7.8, 19.0]

# Middle East
mideast_area = ['Middle East', 24.0, 30.5, 46.0, 52.0]

# Japan
asia_area = ['Japan', 23.5, 45.5, 123.5, 147.0]

regions = [neweng_area, pacnw_area, hawaii_area, westeurope_area,
           southeurope_area, mideast_area, asia_area]


def sort_servers(dictlist, area):
    header = "<h3>" + area[0] + "</h3>\n"
    global sdrlist
    sdrlist = sdrlist + header
    lat_range = [area[1], area[2]]
    lon_range = [area[3], area[4]]
    listcount = 5
    min_snr = 19
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
    for entry in dictlist:
        site_url = entry.get('url')
        site_location = entry.get('loc')
        output = "<a href=\"" + site_url + "/?f=${freq}${bp}${sdrmode}z10\" target=\"_blank\">" + "KiwiSDR, " + site_location + "</a></br>\n"
        sdrlist += output
    return sdrlist


global sdrlist
# build the column of data
sdrlist = "<div>\n"

for area in regions:
    sort_servers(dictlist, area)

# close the column
sdrlist = sdrlist + "</div>\n"

# text to find for first payload
search_text = "8675309"
# replacement text
replace_text = sdrlist

# Opening our text file in read only
# mode using the open() function
with open(final_txt_file, 'r') as file:
    data = file.read()
    data = data.replace(search_text, replace_text)

with open(final_txt_file, 'w') as file:
    file.write(data)
