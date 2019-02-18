[![Build Status](https://travis-ci.org/davipo/openelections-data-wi.svg?branch=master)](https://travis-ci.org/davipo/openelections-data-wi)

# openelections-data-wi
Pre-processed election results for Wisconsin elections

``parser.py`` processes files based on cached metadata in ``local_data_cache/elections_metadata.json``\
To update this metadata from the OpenElections API, run ``python fetch.py wi -m``\
(``fetch.py`` fetches data files based on the cached metadata)

To re-parse data files:
```bash
python parser.py
```

To parse data files for specific elections, append one or more election ids:
```bash
python parser.py 426
```
Elections will be processed in the order they appear in the metadata.

A folder ``local_data_cache`` keeps a local copy of input data files. To update it:
```bash
cd local_data_cache
python fetch.py wi
```

To fetch input files for specific elections, append one or more election ids:
```bash
python fetch.py wi 1577 404
```


Spot tests to check a few records from each results file are in
``wi-elections.feature.csv`` (currently in ``tests/features/`` directory).
To run, use:
```bash
python run_spot_tests.py [<tests_filepath>]
```


Tests to validate the CSV output using <a href="https://github.com/dhcole/csv-test">csv-test</a> can be run (2014 example):
```bash
npm install
node_modules/csv-test/bin/csv-test tests/csv-test-config.yml '2014/*' tests/csv-test-validators.yml
```
