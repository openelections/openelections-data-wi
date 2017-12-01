# Script to fetch OpenElections input files by state and election id

import sys
from httplib import responses           # Python 2.7
# from http.client import responses       # Python 3

import requests


url_base = "http://openelections.net/api/v1/election/"
url_query = "?format=json&limit=0&state__postal="


def save_file(url, filename):
    """Retrieve file at url, save at filename"""
    url = url.strip()
    r = requests.get(url)
    if r.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(r.content)
    else:
        print "Error fetching data file:", r.status_code,
        print responses[r.status_code]
        print "URL =", url


def update_cache(state, id=None):
    """Download data files to update cache
        
        If id, check for correct state (2 letter abbrev) and
            download data files for id;
        else download data files for all elections in state.
    """
    state = state.upper()
    query = url_query + state
    if id == None:
        url = url_base + url_query + state
    else:
        url = url_base + id + '/' + url_query + state
    r = requests.get(url)
    if r.status_code != 200:
        print "Error requesting metadata:", r.status_code,
        print responses[r.status_code]
        print "URL =", url
    else:
        elections = []
        data = r.json()
        if id == None:  # fetch all elections for state
            elections = data.get('objects')
            if not elections:
                print "No elections found for state {}".format(state)
        else:           # fetch a single election, given by id
            state_data = data.get('state')
            postal = state_data.get('postal') if state_data else None
            if postal == state:
                elections = [data]
            else:
                print "Wrong state: id {} is for {}, not {}".format(
                        id, postal, state)
        
        for election in elections:
            if 'direct_links' in election:
                for download_url in election['direct_links']:
                    filename = "data/" + download_url.split('/')[-1]
                    print "Downloading", filename
                    save_file(download_url, filename)
            else:
                msg = "No data files for election id {id} on {start_date}"
                print msg.format(election)



if __name__ == '__main__':
    usage_msg = 'Usage: {} <state_abbrev> [<list of ids>]\n'.format(sys.argv[0])
    usage_msg += '   Fetch data for given election ids in state.\n'
    usage_msg += '   Omit ids to fetch all ids for state.\n'
    args = sys.argv[1:]
    if not args:        # no args
        print usage_msg
    else:
        state = args[0]     # first arg must be two-letter state abbreviation
        if not state.isalpha() or len(state) != 2:
            print usage_msg
        else:
            state = state.upper()
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

