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

cache_path = 'local_data_cache'
metadata_filepath = os.path.join(cache_path, 'elections_metadata.json')
data_path = os.path.join(cache_path, 'data')    # dir to store input files


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


def check_state(election, state):
    """Return True if json election data matches state, else False"""
    state_info = election.get('state')
    postal = state_info.get('postal') if state_info else None
    if postal != state:
        print "\nWrong state: id {} is for {}, not {}".format(
                    election.get('id'), postal, state)
        return False
    return True


def fetch_metadata(state, id=None):
    """Return json metadata for state and id, or None if fails.
        If id, check that fetched election is for correct state.
        If id is None, return metadata for all ids.
    """
    state = state.upper()
    query = url_query + state
    if id == None:
        url = url_base + url_query + state      # all ids
    else:
        url = url_base + str(id) + '/' + url_query + state
    r = request_data(url, error_text='Error requesting metadata:')
    if r is None:
        return None
    metadata = r.json()
    if id is not None:
        if not check_state(metadata, state):
            return None
    return metadata


def read_cached_metadata():
    with open(metadata_filepath) as metadatafile:
        return json.load(metadatafile)


def update_cache(state, ids=None):
    """Download data files to update cache.
        
        If ids (must be a container or None),
            check for correct state (2 letter abbrev) and
            download data files for each election id in ids;
        else download data files for all elections in state.
    """
    elections = []
    metadata = read_cached_metadata()
    if metadata:
        elections = metadata.get('objects')
        if not elections:
            print "No elections found in cached metadata."
    all_ids = not ids   # download all ids if ids is None or empty
    if not all_ids:
        if not all(map(str.isdigit, ids)):      # all digits?
            print 'Error: ids must be positive integers (election ids)'
            return
        ids = map(int, ids)     # convert to ints; & avoid altering parameter
    
    for election in elections:
        id = election.get('id')
        if not all_ids:
            if id not in ids:
                continue   # if ids are specified, skip elections not in list
            ids.remove(id)
        if not check_state(election, state):
            break
        descr = '{start_date} '
        descr += 'special ' if election.get('special') else ''
        descr += '{race_type} election (id {id})'
        descr = descr.format(**election)
        urls = election.get('direct_links')
        if not urls:
            print '\nNo data files for', descr
        else:
            print '\nDownloading input files for', descr
            for download_url in urls:
                filename = os.path.split(download_url)[-1]
                filepath = os.path.join(data_path, filename)
                r = request_data(download_url, 
                                 error_text='Error fetching data file:')
                if r:
                    with open(filepath, 'wb') as f:
                        f.write(r.content)
                    print '   ', filename
    if ids:
        print '\nIds not found in cached metadata:', ids


def update_metadata(state):
    """Fetch metadata for state, cache at metadata_filepath"""
    metadata = fetch_metadata(state)
    if metadata:
        with open(metadata_filepath, 'w') as outfile:
            json.dump(metadata, outfile, indent=3)
        # save a dated copy
        fpath, ext = metadata_filepath.rsplit('.', 1)
        shutil.copy(metadata_filepath, '{}_{}.{}'.format(
                        fpath, datetime.date.today(), ext))


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
                    update_metadata(state)
            else:   # fetch input files
                ids = args[1:]
                if not all(map(str.isdigit, ids)):  # all digits?
                    print usage_msg
                    print 'ids must be positive integers (election ids)'
                else:
                    update_cache(state, ids)
    print

