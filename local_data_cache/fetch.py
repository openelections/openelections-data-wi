import requests
import json
import sys


url_base = "http://openelections.net/api/v1/election/"
url_query = "?format=json&limit=0&state__postal=WI"


def save_file(url, filename):
    url = url.strip()
    r = requests.get(url)
    if r.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(r.content)
    else:
      print "Could not download file %s, status code %s" % (url, r.status_code)


def update_cache(url):
    print url
    url = url.strip()
    r = requests.get(url)
    if r.status_code == 200:
        parsed = json.loads(r.content)['objects']
        for election in parsed:
            if election['direct_links'] == []:
                print "no results for id: ", election['id']
            else:
                for download_url in election['direct_links']:
                    filename = "data/%s" % download_url.split('/')[-1]
                    print "Downloading %s" % filename
                    save_file(download_url, filename)


# Running without args, download all files.
# With args, get files for the ids listed as args.
if __name__ == '__main__':
    args = sys.argv[1:]
    if args:
        if all(map(str.isdigit, args)):
            for arg in args:
                update_cache(url_base + arg + '/' + url_query)
        else:
            print 'Args must be positive integers (election ids)'
    else:
        update_cache(url_base + url_query)

