# -*- coding: utf-8 -*-
import xlrd
import unicodecsv as csv
import requests
import json
import re
import xlrd
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def headers():
  return [["county","ward","office","district","total votes","party","candidate","votes"]]

def process_local(filename,column,results):
    xlsfile = xlsfile = xlrd.open_workbook(filename)
    offices = get_offices(xlsfile,column)
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

def get_election_result(election,column):
  direct_links = election['direct_links'];
  slug = "%s__wi__%s_ward.csv" % (election['start_date'].replace("-",""), election['race_type'])
  year = election['start_date'][:4]
  result_filename = "%s/%s" % (year, slug)
  print "Processing %s" % slug
  myfile = open(result_filename, 'wb')
  wr = csv.writer(myfile)
  results = []
  results.append(headers())
  for direct_link in direct_links:
    cached_filename = "local_data_cache/data/%s" % direct_link.split('/')[-1]
    print "Opening %s" % cached_filename
    results = process_local(cached_filename,column,results)
    for i,result in enumerate(results):
      for x,row in enumerate(result):
        if (x != 0):
          row = clean_particular(election,row)
          row = clean_row(row)
        skip = skip_row(row, "Office Totals:")
        if (skip == 0):
          wr.writerow(row)
    results = []

def clean_county(item):
  return item

def clean_ward(item):
  return item

def clean_office(item):
  return item

def clean_district(item):
  return item

def clean_total(item):
  return to_int(item)

def clean_party(item):
  return item

def clean_votes(item):
  return to_int(item)

def clean_candidate(item):
  return item

def clean_row(row):
  row[0] = clean_county(row[0])
  row[1] = clean_ward(row[1])
  row[2] = clean_office(row[2])
  row[3] = clean_district(row[3])
  row[4] = clean_total(row[4])
  row[5] = clean_party(row[5])
  row[6] = clean_candidate(row[6])
  row[7] = clean_votes(row[7])
  return row

def to_int(item):
  if (item == int(0.0)):
    return 0
  elif (item):
    return int(item)
  else:
    return 0

# Here is where things get messy.
def clean_particular(election,row):
  #if (election['id'] == '1573'):
  return row

def open_file(url, filename):
    r = requests.get(url)
    if r.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(r.content)
    xlsfile = xlrd.open_workbook(filename)
    return xlsfile

# The title page has titles in varying columns.
def get_offices(xlsfile,column=1):
    offices = []
    sheet = xlsfile.sheets()[0]
    last = sheet.nrows-1
    if last == 1:
        rows = [1]
    else:
        rows = range(1,last)
    for i in rows:
        offices.append(sheet.row_values(i)[column])
    return offices

def detect_headers(sheet):
    for i in range(3,12):
        if sheet.row_values(i)[2].strip() == 'Total Votes Cast':
            if 'REP' in sheet.row_values(i) or 'DEM' in sheet.row_values(i) or 'NP' in sheet.row_values(i):
                parties = [x for x in sheet.row_values(i)[3:] if x != None]
                candidates = [x for x in sheet.row_values(i+1)[3:] if x!= None]
                start_row = i+2
            else:
                parties = sheet.row_values(i-1)[3:]
                candidates = sheet.row_values(i)[3:]
                start_row = i+1
            return [zip(candidates, parties), start_row]
        else:
            continue

def parse_sheet(sheet, office):
    output = []
    combo, start_row = detect_headers(sheet)
    if 'DISTRICT' in office.upper():
        # This '–' is a different character than this '-'
        office = office.replace('–','-')
        split = office.split('-')
        # Office string comes in formats:
        #  * STATE SENATE - DISTRICT 1 - REPUBLICAN
        #  * STATE SENATE   DISTRICT 1 - REPUBLICAN
        if (len(split) == 2):
            try:
                office, district = office.split('-')
            except:
                office, district = office.split(u'-')
        # Assumes STATE SENATE - DISTRICT 1 - REPUBLICAN format
        else:
          try:
              office, district, party  = office.split('-')
          except:
              office, party, district = office.split(u'-')
        district = district.replace('DISTRICT ','')
    else:
        district = office
    if len(office.split(",")) > 1:
      party = district
      district = office.split(",")[1]
      office = office.split(",")[0]
    county = ''
    for i in range(start_row, sheet.nrows):
        results = sheet.row_values(i)
        if "Totals" in results[1]:
            continue
        if results[0].strip() != '':
            county = results[0].strip()
        elif(len(district.split(" COUNTY ")) > 1):
          county = office.split(" COUNTY ")[0]
        else:
          county = county
        ward = results[1].strip()
        total_votes = int(results[2]) if results[2] else results[2]
        # Some columns are randomly empty.
        candidate_votes = results[3:]
        for candidate, party in combo:
            index = [x[0] for x in combo].index(candidate)
            if (candidate == None or candidate == ''):
                continue
            else:
                output.append([county, ward, office, district, total_votes, party, candidate, candidate_votes[index]])
    return output

def remove_empty_column(row):
  cleaned = []
  for i,item in enumerate(row):
    if (item != ''):
      cleaned.append(item)
  return cleaned

  return cleaned

def process_all(url, filename):
    results = []
    xlsfile = open_file(url, filename)
    offices = get_offices(xlsfile)
    for office in offices:
        index = [x for x in offices].index(office)
        sheet = xlsfile.sheets()[index+1]
        results.append(parse_sheet(sheet, office))

    return [r for result in results for r in result]

def get_all_results(ids,url,column=1):
  r = requests.get(url)
  if r.status_code == 200:
    parsed = json.loads(r.content)['objects']
    for id in ids:
      print "id %s" % id
      for election in parsed:
        if election['id'] == id:
          get_election_result(election,column)

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
working_ids_no_test = [404,405,407,408,409,411,413,415,416,424,674,685]
working_ids_column_1_no_test = [1575,1539,404,405,407,408,409,411,413,415,416,424,674,685]

# For local testing
working_ids_with_tests = [1574,1661,1658,1660,1659,1576,1573]
#test = [1575]

get_all_results(working_ids_with_tests,WIOpenElectionsAPI)
#get_all_results(test,WIOpenElectionsAPI,0)
