# -*- coding: utf-8 -*-
from wigab.parser import get_offices
from wigab.parser import parse_sheet
from wigab.parser import process_all
import xlrd
import unicodecsv as csv
import pprint
import requests
import json
import re

def headers():
  return [["county","ward","office","district","total votes","party","candidate","votes"]]

def process_local(filename,column):
    results = []
    xlsfile = xlsfile = xlrd.open_workbook(filename)
    offices = get_offices(xlsfile,column)
    results.append(headers())
    for office in offices:
        index = [x for x in offices].index(office)
        sheet = xlsfile.sheets()[index+1]
        results.append(parse_sheet(sheet, office))
    return results

def skip_row(row, skip_str):
  skip = 0
  for item in row:
    if (item == "Office Totals:"):
      skip = 1
  return skip

def get_election_result(election,local,column):
  direct_links = election['direct_links'];
  slug = "%s__wi__%s_ward.csv" % (election['start_date'].replace("-",""), election['race_type'])
  year = election['start_date'][:4]
  print "Processing %s" % slug
  for direct_link in direct_links:
    if local is None:
      download_filename = "temp"
      results = process_all(direct_link, download_filename)
    else:
      cached_filename = "local_data_cache/data/%s" % direct_link.split('/')[-1]
      print "Opening %s" % cached_filename
      results = process_local(cached_filename,column)
    result_filename = "%s/%s" % (year, slug)
    myfile = open(result_filename, 'wb')
    wr = csv.writer(myfile)
    for result in results:
      for row in result:
        skip = skip_row(row, "Office Totals:")
        if (skip == 0):
          wr.writerow(row)

def get_all_results(ids,url,local=None,column=1):
  r = requests.get(url)
  if r.status_code == 200:
    parsed = json.loads(r.content)['objects']
    for id in ids:
      print "id %s" % id
      for election in parsed:
        if election['id'] == id:
          get_election_result(election,local,column)

WIOpenElectionsAPI = "http://openelections.net/api/v1/election/?format=json&limit=0&state__postal=WI"
# All ids from available elections.
available_ids = [1658, 1659, 1660,1661,1576,1573,1574,1575,1538,1539,404,405,
407,408,409,410,411,1662,413,415,416,419,421,422,424,425,426,427,428,429,430,
431,432,433,434,435,436,437,438,439,440,441,442,443,444,445,446,447,448,664,
674,685,689,1577,1578]

# Elections with no files available.
no_results_ids = [446, 674, 685, 689]
# Not working ids. Need to troubleshoot.
not_working_ids = [410,421,419,422,
425,426,427,428,429,430,431,432,433,434,435,436,
437,438,439,440,441,442,443,444,445,446,447,448,
689,1577,1578]
# Election with PDF files.
pdf_elections = [664]
# 1662 has a sheet with no cover sheet unlike others.
need_custom_function = [1662]

# List of ids for elections that have been successfully processed.
working_ids_no_test = [1659,1576,1573,404,405,407,408,409,411,413,415,416,424,674,685]
working_ids_column_1_no_test = [1575,1539,404,405,407,408,409,411,413,415,416,424,674,685]

# For local testing
working_ids_with_tests = [1574,1661,1658,1660]

get_all_results(working_ids_with_tests,WIOpenElectionsAPI,True)
#get_all_results(test_ids,WIOpenElectionsAPI,True,0)
