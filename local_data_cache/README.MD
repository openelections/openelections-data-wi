## Local copies of WI Election files

This folder contains local cached copies of WI election data,
from http://elections.wi.gov \
(Some files may be from the former location http://www.gab.wi.gov)

This is useful for testing ``parser.py`` (in the parent directory),
without requesting the input files via http every time.

``fetch.py`` (in parent directory) can be used to update the local cache. (See README there.)

``elections_metadata.json`` caches elections metadata from the OpenElections API.\
To update it, run ``python fetch.py wi -m``
