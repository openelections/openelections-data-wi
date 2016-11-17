[![Build Status](https://travis-ci.org/davipo/openelections-data-wi.svg?branch=master)](https://travis-ci.org/davipo/openelections-data-wi)

# openelections-data-wi
Pre-processed election results for Wisconsin elections

To re-parse files:
```bash
python parser.py
```

A folder ``local_data_cache`` keeps a local version of files. To update it:

```bash
cd local_data_cache
python fetcher.py
```

There are two types of tests:

1. Tests to validate the CSV output using <a href="https://github.com/dhcole/csv-test">csv-test</a>. To test:
```bash
npm install
node_modules/csv-test/bin/csv-test tests/csv-test-config.yml '2014/*' tests/csv-test-validators.yml
```

2. Tests to validate a sampling of results. These use behave and follow the format:
```yml
Examples: 20150929__wi__general_ward.csv
  | candidate                   | office   | ward                           | votes  | total |
  | Cindi Duchow                | Assembly | Village of Hartland Wards 1-13 | 117    | 140   |
  | Thomas D. Hibbard (Write-In)| ASSEMBLY | Village of Wales Wards 1-4     | 10     | 106   |
```

To run those tests ``cd tests; behave``  
