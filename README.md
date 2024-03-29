# kiwisdr-helpers

Parse, filter, and sort kiwisdr site data and generate html lists.

### Purpose:

These scripts are written to parse the data file which lists the publicly accessible KiwiSDR servers at [kiwisdr.com/public](http://kiwisdr.com/public/) and used by [Dyatlov Mapmaker](https://github.com/priyom/dyatlov). After parsing raw KiwiSDR data, the scripts sort, filter, and restructure the data as html for building web pages. They build working pages by substituting current data into templates.

You can do a lot of things with the methods you'll find in this code. For every kind of monitoring niche, there is a way to build up a list of the most suitable radios. Downloading the current SDR data takes several seconds on modest broadband, but processing it with these scripts is very fast - well under a second on the server.

### Files:

#### stripper:
Written in Bash; parses kiwisdr_com.js and creates a Python list of dictionaries for use by other scripts. It also runs those other scripts.

#### kiwisdr_best.py:
Written in Python; parses data in kiwisdr_stripped.py, filters and sorts sites by snr score, and writes links into an html file. Builds the basic [Best KiwiSDR Server List](https://skywavelinux.com/best-sdrservers.html).

#### hfgcs_updater.py:
Written in Python; parses data in kiwisdr_stripped.py, filters and sorts sites by snr score, further filters by geographical area, then and writes links into an html file. Builds the [Quick Tune HFGCS List](https://skywavelinux.com/hfgcs-quick-tune-list.html).

#### volmet_updater.py:
Written in Python; parses data in kiwisdr_stripped.py, filters and sorts sites by snr score, further filters by geographical area, then and writes links into an html file. Builds the [VOLMET Quick Tune SDR List](https://skywavelinux.com/quicktune-volmets.html).

#### canada_updater.py:
Written in Python; parses data in kiwisdr_stripped.py, filters and sorts sites by snr score, further filters by geographical area, then and writes links into an html file. Builds the [KiwiSDR Canada List](https://skywavelinux.com/kiwisdr-canada.html)).

#### ausnz_updater.py:
Written in Python; parses data in kiwisdr_stripped.py, filters and sorts sites by snr score, further filters by geographical area, then and writes links into an html file. Builds the [KiwiSDR Australia and New Zealand List](https://skywavelinux.com/kiwisdr-ausnz.html).

#### hf_aero_redirects.py
Written in Python; parses data in kiwisdr_stripped.py, filters and sorts sites by snr score, further filters by geographical area, then and writes files containing php redirects to KiwiSDRs. Capable of switching frequencies based on day / night time. Builds the [HF Aero Redirects](https://skywavelinux.com/hf-aero0) and more.

#### sdr_redirects.py
Written in Python; parses data in kiwisdr_stripped.py, filters and sorts sites by snr score, further filters by geographical area, then and writes files containing php redirects to KiwiSDRs. Capable of switching frequencies based on day / night time, mode setting. Builds the [SDR Redirects](https://www.ab9il.net/monitor0) and more.

#### sdr-stream:
*This script has been incorporated into _supersdr-wrapper_. Use _supersdr-wrapper_ to select from a sorted list of KiwiSDR servers or your preselected KiwiSDR bookmarks*.
