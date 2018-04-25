# Script to fetch OpenElections input files by state and election id

import datetime
from httplib import responses           # Python 2.7
# from http.client import responses       # Python 3
import json
import os
import shutil
import sys

import requests


url_base = "http://openelections.net/api/v1/election/"
url_query = "?format=json&limit=0&state__postal="

cache_path = ''
metadata_filepath = os.path.join(cache_path, 'elections_metadata.json')
data_path = os.path.join(cache_path, 'data')    # path to input files


def request_data(url, error_text='Error requesting data:'):
    """Retrieve data at url, return requests object, or None if fails"""
    url = url.strip()
    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as exc:
        print error_text
        print exc
        print "URL =", url
        return None
    if r.status_code != 200:
        print error_text,
        print r.status_code, responses[r.status_code]
        print "URL =", url
        return None
    return r


def fetch_metadata(state, id=None):
    """Return json metadata for state and id, or None if fails.
        If id is None, return metadata for all ids.
    """
    state = state.upper()
    query = url_query + state
    if id == None:
        url = url_base + url_query + state      # all ids
    else:
        url = url_base + id + '/' + url_query + state
    r = request_data(url, error_text='Error requesting metadata:')
    return r.json() if r else None


def read_cached_metadata():
    with open(metadata_filepath) as metadatafile:
        return json.load(metadatafile)


def update_cache(state, id=None):
    """Download data files to update cache.
        
        If id, check for correct state (2 letter abbrev) and
            download data files for id;
        else download data files for all elections in state.
    """
    elections = []
    metadata = fetch_metadata(state, id)
    if metadata:
        if id == None:  # fetch all elections for state
            elections = metadata.get('objects')
            if not elections:
                print "No elections found for state {}".format(state)
        else:  # fetching a single election, given by id: check state
            state_data = metadata.get('state')
            postal = state_data.get('postal') if state_data else None
            if postal == state:
                elections = [metadata]
            else:
                print "Wrong state: id {} is for {}, not {}".format(
                        id, postal, state)
    
    for election in elections:
        print
        if 'direct_links' in election:
            print 'Downloading input files for election id', election['id']
            for download_url in election['direct_links']:
                filename = os.path.split(download_url)[-1]
                filepath = os.path.join(data_path, filename)
                r = request_data(download_url, 
                                 error_text='Error fetching data file:')
                if r:
                    with open(filepath, 'wb') as f:
                        f.write(r.content)
                    print '   ', filename
        else:
            msg = "No data files for election id {id} on {start_date}"
            print msg.format(election)


if __name__ == '__main__':
    usage_msg = 'Usage: {} <state_abbrev> [-m | <list of ids>]\n'
    usage_msg += '   Fetch input files for given election ids in state.\n'
    usage_msg += '   Omit ids to fetch all ids for state.\n'
    usage_msg += '   Option -m fetches metadata, caches it in "{}".\n'
    usage_msg = usage_msg.format(sys.argv[0], metadata_filepath)
    args = sys.argv[1:]
    if not args:
        print usage_msg
    else:
        state = args[0]
        if not state.isalpha() or len(state) != 2:
            print usage_msg
            print 'First arg must be two-letter state abbreviation'
        else:
            state = state.upper()
            if args[1:2] == ['-m']:     # fetch and cache metadata
                if len(args) > 2:
                    print usage_msg
                    print 'args not permitted after -m'
                else:
                    metadata = fetch_metadata(state)
                    if metadata:
                        with open(metadata_filepath, 'w') as outfile:
                            json.dump(metadata, outfile, indent=4)
                        # save a dated copy
                        fpath, ext = metadata_filepath.rsplit('.', 1)
                        shutil.copy(metadata_filepath, '{}_{}.{}'.format(
                                        fpath, datetime.date.today(), ext))
            else:
                ids = args[1:]
                if not ids:     # fetch all ids for state
                    update_cache(state)
                else:
                    if all(map(str.isdigit, ids)):      # all digits
                        for id in ids:
                            update_cache(state, id)
                    else:
                        print usage_msg
                        print 'ids must be positive integers (election ids)'
    print

