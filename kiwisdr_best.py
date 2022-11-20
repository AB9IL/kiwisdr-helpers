#!/usr/bin/env python3

import shutil
from kiwisdr_stripped import dictlist

# purpose: build a list of KiwiSDRs
# filtered and sorted by snr
# rewrites list as html for website

# file for inclusion in html
origin_txt_file = "../best-sdrservers.html.orig"
final_txt_file = "../best-sdrservers.html"
websdr_file = "websdr_best.html"
shutil.copy(origin_txt_file, final_txt_file)

# filter the list of dictionaries by snr
listcount = 50
min_snr = 19
mykeys = ['url', 'loc']
sdrlist = []
filtered_dict = list(filter(lambda site: int(site["snr"][-2:].replace(',', ''))
                            > min_snr, dictlist))

# sort the list of dicts by snr and truncate
filtered_dict.sort(key=lambda item: item.get("snr"), reverse=True)
filtered_dict = filtered_dict[0:listcount]

for entry in filtered_dict:
    result = []
    for item in mykeys:
        val = entry.get(item)
        result.append(val)
    sdrlist.append(result)

# build the first column of data
payload_1 = "<div class=\"column\">\n"
for element in sdrlist:
    output ="<a href=\"" + element[0] + "/?f=${freq}${bp}${sdrmode}z10\" target=\"_blank\">" + "KiwiSDR, " + element[1] + "</a></br>\n"
    payload_1 = payload_1 + output
payload_1 = payload_1 + "</div>\n"

# text to find for first payload
search_text = "8675309"
# replacement text
replace_text = payload_1

# text to find for second payload
search2_text = "9035768"
# second block of replacement text
with open(websdr_file) as file2:
   replace2_text = file2.read()

# Opening our text file in read only
# mode using the open() function
with open(final_txt_file, 'r') as file:
    data = file.read()
    data = data.replace(search_text, replace_text)
    data = data.replace(search2_text, replace2_text)

with open(final_txt_file, 'w') as file:
    file.write(data)
