# -*- coding: utf-8 -*-

import json
import re
import sys

import requests
import six
import unicodecsv as csv
import xlrd

reload(sys)
sys.setdefaultencoding('utf8')

party_list = ['IND', 'REP', 'DEM', 'NA', 'NP', 'CON', 'WIG', 'LIB']

headers = ["county","ward","office","district","total votes","party","candidate","votes"]


def process_local(filename, column):
    xlsfile = xlrd.open_workbook(filename)
    offices = get_offices(xlsfile,column)
    results = []
    for office in offices:
        index = [x for x in offices].index(office)
        sheet = xlsfile.sheets()[index+1]
        results.append(parse_sheet(sheet, office))
    return results


def get_election_result(election,column):
  direct_links = election['direct_links'];
  slug = "%s__wi__%s_ward.csv" % (election['start_date'].replace("-",""), election['race_type'])
  year = election['start_date'][:4]
  result_filename = "%s/%s" % (year, slug)
  print "Processing %s" % slug
  myfile = open(result_filename, 'wb')
  wr = csv.writer(myfile)
  wr.writerow(headers)
  for direct_link in direct_links:
    cached_filename = "local_data_cache/data/%s" % direct_link.split('/')[-1]
    print "Opening %s" % cached_filename
    results = process_local(cached_filename, column)
    for i,result in enumerate(results):
      for x,row in enumerate(result):
        row = clean_particular(election,row)
        row = clean_row(row)
        if "Office Totals:" not in row:
          wr.writerow(row)
    results = []

def clean_county(item):
  return clean_string(item)

def clean_ward(item):
  return clean_string(item)

def clean_office(item):
  return clean_string(item)

def clean_district(item):
  item = clean_string(item)
  if (re.match(r"^[0-9,]*$",item)):
    return to_int(item)
  else:
    return None

def clean_total(item):
  return to_int(item)

def clean_party(item):
  return item

def clean_votes(item):
  return to_int(item)

def clean_candidate(item):
  return clean_string(item)

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
    try:
      int(item)
      return int(item)
    except ValueError:
      item = item.replace(",","")
      return int(item)
  else:
    return 0

def clean_string(item):
  item = item.strip()
  item = item.replace("\n"," ")
  item = item.title()
  return item

# Here is where things get messy.
def clean_particular(election,row):
  # Removes district.
  if (election['id'] == 404 or election['id'] == 405):
    row[3] = ''
  elif (election['id'] == 411 or election['id'] == 413):
    row[1] = row[1].replace("!","1")
  elif (election['id'] == 424):
    row[2] = row[2].replace(" - 2011-2017","")
    row[3] = ''
  elif (election['id'] == 1662):
    row[2] = row[2].replace("RECALL ","")
    row[2] = row[2].replace("- 13","")
    row[2] = row[2].replace("- 21","")
    row[2] = row[2].replace("- 23","")
    row[1] = row[1].replace("!","1")

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
    sheet = xlsfile.sheet_by_index(0)
    return sheet.col_values(column)


def any_party_in(sequence):
    """ Return True if any party abbreviation is an element of sequence, else False.
        Uses abbreviations in party_list.
    """
    for party in party_list:
        if party in sequence:
            return True
    return False


def detect_headers(sheet):
    for i in range(3,12):
        row = sheet.row_values(i)
        if row[2].strip() == 'Total Votes Cast':
            if any_party_in(row):
                parties = [x for x in row[3:] if x != None]
                candidates = [x for x in sheet.row_values(i+1)[3:] if x!= None]
                start_row = i+2
            else:
                parties = sheet.row_values(i-1)[3:]
                candidates = row[3:]
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
        elif len(district.split(" COUNTY ")) > 1:
          county = office.split(" COUNTY ")[0]
        ward = results[1].strip()
        if isinstance(results[2], six.string_types):
          results[2] = results[2].replace(",","")
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
no_results_ids = [674, 685, 689,448]
# File won't open
bad_file = [440]
# Election with PDF files.
pdf_elections = [
446,664,410,422,443,
445,447]
# Has a sheet with no cover sheet unlike others.
need_custom_function = [
1662,421,1577,1578,430,
431,432,434,435,436,
438,439,441,442,444,
426,427,428,429,433]
zip_file = [437]

# List of ids for elections that have been successfully processed.
# 22
working = [
1574,1661,1658,1660,1659,
1576,1573]
working_column_1 = [
1539,405,404,407,408,
409,411,413,415,416,
419,1575,424,425,1662]

get_all_results(working,WIOpenElectionsAPI)
get_all_results(working_column_1,WIOpenElectionsAPI,0)
