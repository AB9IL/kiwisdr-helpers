#!/usr/bin/env python3

import shutil
from kiwisdr_stripped import dictlist

# file for inclusion in html
origin_txt_file = "../kiwisdr-ausnz.html.orig"
final_txt_file = "../kiwisdr-ausnz.html"
shutil.copy(origin_txt_file, final_txt_file)

# filter the list of dictionaries by latitude longitude
# use geographic boxes bounded by: (south, north, west, east)
# Adelaide, SAU
adelaide_area = ['--Adelaide--', -36.0, 32.5, 135.0, 141.0]

# Auckland, AUK
auckland_area = ['--Auckland--', -39.0, -34.0, 172.0, 179.0]

# Brisbane, QLD
brisbane_area = ['--Brisbane--', -28.3, -25.3, 151.0, 154.0]

# Burnie, TAS
burnie_area = ['--Burnie--', -44.3, -39.3, 143.0, 149.0]

# Canberra, NSW
canberra_area = ['--Canberra--',  -36.5, -34.7, 147.0, 151.0]

# Christchurch, CAN
christchurch_area = ['--Christchurch--',  -44.5, -42.0, 169.0, 174.5]

# Darwin, NT
darwin_area = ['--Darwin--',  -16.0, -10.0, 129.0, 137.0]

# Melbourne, VIC
melbourne_area = ['--Melbourne--',  -39.4, -36.0, 142.0, 147.0]

# Newcastle, NSW
newcastle_area = ['--Newcastle--',  -33.5, -31.5, 149.5, 153.0]

# Perth, WA
perth_area = ['--Perth--', -33.5, -30.0, 114.0, 119.5]

# Sydney, NSW
sydney_area = ['--Sydney--',  -35.0, -32.5, 149.5, 152.0]

# Wellington, WGN
wellington_area = ['--Wellington--', -42.5, -38.7, 171.0, 179.0]

regions = [adelaide_area, auckland_area, brisbane_area, burnie_area,
           canberra_area, christchurch_area, darwin_area, melbourne_area,
           newcastle_area, perth_area, sydney_area, wellington_area]


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
