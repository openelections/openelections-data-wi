[![Build Status](https://travis-ci.org/acouch/openelections-data-wi.svg?branch=master)](https://travis-ci.org/acouch/openelections-data-wi)

# openelections-data-wi
Pre-processed election results for Wisconsin elections

To re-parse files:
```bash
git submodule update --init
python parser.py
```

A folder ``local_data_cache`` keeps a local version of files. To update it:

```bash
cd local_data_cache
python fetcher.py
```

There are tests to validate the CSV output using <a href="https://github.com/dhcole/csv-test">csv-test</a>. To test:
```bash
npm install
node_modules/csv-test/bin/csv-test csv-test-config.yml 2014/20141104__wi__general_ward.csv csv-test-validators.yml
```
