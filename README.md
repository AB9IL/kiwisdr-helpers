# kiwisdr-helpers

Parse, filter, and sort kiwisdr site data and generate html lists.

### Purpose:

These scripts are written to parse the data file which lists the publicly accessible KiwiSDR servers at [kiwisdr.com/public](http://kiwisdr.com/public/) and used by [Dyatlov Mapmaker](https://github.com/priyom/dyatlov). After parsing raw KiwiSDR data, the scripts sort, filter, and restructure the data as html for building web pages. They build working pages by substituting current data into templates.

### Files:

#### stripper:
Written in Bash; parses kiwisdr_com.js and creates a Python list of dictionaries for use by other scripts. It also runs those other scripts.

#### kiwisdr_best.py:
Written in Python; parses data in kiwisdr_stripped.py, filters and sorts sites by snr score, and writes links into an html file. Builds the basic [Best KiwiSDR Server List](https://skywavelinux.com/best-sdrservers.html).

#### hfgcs_updater.py:
Written in Python; parses data in kiwisdr_stripped.py, filters and sorts sites by snr score, further filters by geographical area, them and writes links into an html file. Builds the [Quick Tune HFGCS List](https://skywavelinux.com/hfgcs-quick-tune-list.html).

#### volmet_updater.py:
Written in Python; parses data in kiwisdr_stripped.py, filters and sorts sites by snr score, further filters by geographical area, them and writes links into an html file. Builds the [VOLMET Quick Tune SDR List](https://skywavelinux.com/quicktune-volmets.html).
