[![Build Status](https://travis-ci.org/acouch/openelections-data-wi.svg?branch=master)](https://travis-ci.org/acouch/openelections-data-wi)

# openelections-data-wi
Pre-processed election results for Wisconsin elections

To test/re-parse files:
```bash
git submodule update --init
touch wigab/__init__.py
python parser.py
```

A folder ``local_data_cache`` can be used to fetch remote files for troubleshooting parsing results.
