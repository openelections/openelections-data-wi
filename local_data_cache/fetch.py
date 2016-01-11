import requests
import json

WIOpenElectionsAPI = "http://openelections.net/api/v1/election/?format=json&limit=0&state__postal=WI"

def save_file(url, filename):
    r = requests.get(url)
    if r.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(r.content)
    else:
      print "Could not download file %s, status code %s" % (url, r.status_code)

def update_cache(url):
  r = requests.get(url)
  if r.status_code == 200:
    parsed = json.loads(r.content)['objects']
    for i in parsed:
      if i['direct_links'] == []:
        print "no results for id: ",i['id']
      else:
        for download_url in i['direct_links']:
          filename = "data/%s" % download_url.split('/')[-1]
          print "Downloading %s" % filename
          save_file(download_url, filename)

update_cache(WIOpenElectionsAPI)
