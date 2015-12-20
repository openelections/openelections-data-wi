import requests
import pprint
import json
import wget

WIOpenElectionsAPI = "http://openelections.net/api/v1/election/?format=json&limit=0&state__postal=WI"

def update_cache(url):
    r = requests.get(url)
    if r.status_code == 200:
        parsed = json.loads(r.content)['objects']
        for i in parsed:
            if i['direct_links'] == []:
                print "no results for id: ",i['id']
            else:
                url = i['direct_links'][0]
                wget.download(url)


update_cache(WIOpenElectionsAPI)
