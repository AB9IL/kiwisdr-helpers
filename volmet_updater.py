#!/usr/bin/env python3

import shutil
from kiwisdr_stripped import dictlist

# purpose: build a list of KiwiSDRs
# for VOLMET (aviation weather) monitoring
# filtered and sorted by snr
# and regions defined by latitude / longitude
# rewrites list as html for website

# file for inclusion in html
origin_txt_file = "../quicktune-volmets.html.orig"
final_txt_file = "../quicktune-volmets.html"
shutil.copy(origin_txt_file, final_txt_file)

# filter the list of dictionaries by latitude longitude
# use geographic boxes bounded by: (south, north, west, east)
# Gander, Canada
gander_area = ['--Gander--',
               42.5, 60.0, -83.0, -50.0]

# Shannon, Ireland
shannon_area = ['--Shannon--',
                49.5, 60.0, -12.0, 4.0]

# Tokyo,
tokyo_area = ['--Tokyo--',  23.5, 45.5, 123.5, 147.0]

# Hong Kong
hk_area = ['--HongKong--',  7.3, 27.5, 118.5, 130.0]

# Auckland
aunz_area = ['--Auckland--',  -49.0, -32.0, 163.0, 187.0]

# Australia
aust_area = ['--Australia--',  23.5, 45.5, 123.5, 147.0]

# Beijing and Guangzhou
bjgz_area = ['--BeijingGuangzhou--', 7.3, 27.5, 118.5, 130.0]

# South Asia
sa_area = ['--SouthAsia--', -11.5, 30.0, 66.0, 131.0]

# La Paz
lapaz_area = ['--LaPaz--', -43.0, 12.0, -82.0, -34.0]

# Resistencia
resistencia_area = ['--Resistencia--', -70.0, -11.0, -82.0, -40.0]

# Petersburg and Rostov
peter_rost_area = ['--StPetersburgRostov--', 47.0, 71.0, -29.0, 60.0]

regions = [gander_area, shannon_area, tokyo_area, hk_area, aunz_area,
           aust_area, bjgz_area, sa_area, lapaz_area, resistencia_area,
           peter_rost_area]


def sort_servers(area):
    global sdrlist
    sdrlist = ''
    lat_range = [area[1], area[2]]
    lon_range = [area[3], area[4]]
    listcount = 5
    min_snr = 19
    filtered_dict = list(filter(lambda site: int(site["snr"][-2:].replace(',', ''))
                                > min_snr, dictlist))
    # sort the list of dicts by snr, latitude, and longitude
    filtered_dict.sort(key=lambda item: item.get("snr"), reverse=True)
    filtered_dict = list(filter(lambda site: float(site["gps"].split(',')[0][1:])
                                > lat_range[0], filtered_dict))
    filtered_dict = list(filter(lambda site: float(site["gps"].split(',')[0][1:])
                                < lat_range[1], filtered_dict))
    filtered_dict = list(filter(lambda site: float(site["gps"].split(',')[1][:-1])
                                > lon_range[0], filtered_dict))
    filtered_dict = list(filter(lambda site: float(site["gps"].split(',')[1][:-1])
                                < lon_range[1], filtered_dict))
    # truncate the list
    filtered_dict = filtered_dict[0:listcount]
    # build the list of servers
    for entry in filtered_dict:
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
    sort_servers(area)
    # close the column
    # text to find for first payload
    search_text = area[0]
    # replacement text
    replace_text = sdrlist
    data = data.replace(search_text, replace_text)

with open(final_txt_file, 'w') as file:
    file.write(data)
