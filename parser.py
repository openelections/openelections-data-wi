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

offices_without_title_sheet = ['JUSTICE OF THE SUPREME COURT']

def process_local_xls_2002_to_2010(filename):
    results = []
    xlsfile = xlsfile = xlrd.open_workbook(filename)
    sheet = xlsfile.sheets()[0]
    last = sheet.nrows-1
    candidates = range(17,sheet.ncols)
    start_row = 2
    candiate_row = 0
    skip_rows = 0
    for candidate in candidates:
      for i in range(start_row, sheet.nrows-1):
        # SOME of the sheets have multiple results separated by TOTAL
        if (sheet.row_values(i)[16] == "TOTAL"):
          candiate_row = i + 1
          skip_rows = 3
        # Need to skip to 2 rows after TOTAL
        if (skip_rows):
          skip_rows -= 1
          continue
        candidate_name =  sheet.row_values(candiate_row)[candidate]
        if (candidate_name == ''):
          continue
        total_votes = 0
        county = sheet.row_values(i)[10]
        ward = "%s of %s %s" % (sheet.row_values(i)[11],sheet.row_values(i)[13],sheet.row_values(i)[16])
        office = sheet.row_values(i)[4]
        district = str(sheet.row_values(i)[5])
        for vote in candidates:
          if (sheet.row_values(i)[vote]):
            total_votes += sheet.row_values(i)[vote]
        party = sheet.row_values(candiate_row+1)[candidate]
        votes = sheet.row_values(i)[candidate]
        row = [county,ward,office,district,total_votes,party,candidate_name,votes]
        results.append(row)
    return [results]

def process_local(filename):
    xlsfile = xlrd.open_workbook(filename)
    offices = get_offices(xlsfile)
    results = []
    if offices:
        for i, office in enumerate(offices):
            sheet = xlsfile.sheet_by_index(i + 1)
            results.append(parse_sheet(sheet, office))
    else:
        # no offices found, assume first sheet is not a title sheet
        sheet = xlsfile.sheet_by_index(0)
        for office in offices_without_title_sheet:
            # Look for an office in first column, search first 12 rows
            if office in sheet.col_values(colx=0, start_rowx=0, end_rowx=12):
                results.append(parse_without_title_sheet(sheet, office))
                break
    return results


def process_offices_test(filename):
    xlsfile = xlrd.open_workbook(filename)
    offices = get_offices(xlsfile)
    for office in offices:
        parse = parse_office(office)
#         if len(parse[2]) not in (1, 2):
        print '{:65} {}'.format(office, parse)
    print
    return []


def prep_election_results(election):
    type = election['race_type']
    if (election['special']):
        type = "special_%s" % (type)
    slug = "%s__wi__%s_ward.csv" % (election['start_date'].replace("-",""), type)
    year = election['start_date'][:4]
    result_filename = "%s/%s" % (year, slug)
    print "Processing %s" % slug
    myfile = open(result_filename, 'wb')
    return myfile

def get_election_result(election, process_function=process_local):
  if process_function != process_offices_test:
    myfile = prep_election_results(election)
    wr = csv.writer(myfile)
    wr.writerow(headers)
  direct_links = election['direct_links']
  for direct_link in direct_links:
    cached_filename = "local_data_cache/data/%s" % direct_link.split('/')[-1]
    print "Opening %s" % cached_filename
    results = process_function(cached_filename)
    if process_function == process_offices_test:
        continue
    for i,result in enumerate(results):
      for x,row in enumerate(result):
        row = clean_particular(election,row)
        row = clean_row(row)
        if "Office Totals:" not in row:
          wr.writerow(row)

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

### revise to simplify?
### will still raise ValueError if item contains non-digit non-comma chars
# def to_int(item):
#     if not item:    # 0 or ''
#         return 0
#     else:
#         try:
#             return int(item)
#         except ValueError:
#             item = item.replace(",","")
#             return int(item)

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
  elif (election['id'] == 442):
    row[5] = row[5].replace("Non-Partisan", "NP")
  elif (election['id'] == 1577 or election['id'] == 1578):
    office = None
    # Fetches office name from: "State Assembly, District No. 89"
    office = re.search("(^[A-Za-z ]+)", row[2])
    if office:
      row[2] = office.group(1)
    row[5] = row[5].replace("Democratic", "DEM")
    row[5] = row[5].replace("Republican", "REP")
    row[5] = row[5].replace("Wisconsin Green", "WGR")
    row[5] = row[5].replace("Libertarian", "LIB")
    row[5] = row[5].replace("Independent", "IND")
    row[5] = row[5].replace("Constitution", "CON")
    row[6] = row[6].replace("/"," &")

  return row

def open_file(url, filename):
    r = requests.get(url)
    if r.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(r.content)
    xlsfile = xlrd.open_workbook(filename)
    return xlsfile

def get_offices(xlsfile):
    sheet = xlsfile.sheet_by_index(0)
    # Title page may have offices in column A or B (0 or 1), detect which column
    column = 0 if sheet.cell_value(1, 0) else 1
    offices = sheet.col_values(column)[1:]     # skip first row
    if offices[0] == '':    # if first office empty,
        offices = []            # assume not a title sheet, no offices
### Next line will simulate bug in 2016-02-14 version that skips last row if > 1 rows
###    offices = offices[:-1] if len(offices) > 1 else offices
    return offices

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
            return candidates, parties, start_row


def parse_office(office_string):
    """ Parse office string, returning (office, county, district, party)
        
        Office string comes in many formats:
          LIEUTENANT GOVERNOR
          US SENATOR - AMERICANS ELECT
          PRESIDENT OF THE UNITED STATES - REPUBLICAN PARTY
          ASSEMBLY - DISTRICT 99
          STATE SENATE - DISTRICT 1 - REPUBLICAN
          STATE SENATE   DISTRICT 1 - REPUBLICAN
          REPRESENTATIVE TO THE ASSEMBLY,  DISTRICT 99 - REPUBLICAN
          REPRESENTATIVE TO THE ASSEMBLY, DISTRICT 99 WISCONSIN GREEN
          District Attorney - Fond Du Lac County
          EAU CLAIRE COUNTY CIRCUIT COURT JUDGE, BRANCH 1
          RECALL STATE SENATE-29
    """
    office = str(office_string).upper()
    office = office.replace('―','-')    # change \u2015 HORIZONTAL BAR to hyphen
    office = office.replace('–', '-')   # change \u2013 EN DASH to hyphen
    
    if ' DISTRICT ' in office:
        head, sep, tail = office.partition(' DISTRICT ')
        office = head.strip(',- ')
        district, sep, party = tail.partition(' ')
        party = party.strip('- ')
    else:
        district = 'clean to None'
        party = ''
    
    # extract county if found
    county = ''
    head, sep, tail = office.partition(' COUNTY')
    if sep:             # county found
        if tail == '':    # some office – some county COUNTY
            office, sep, county = head.partition('-')
            county = county.strip()
#         else :   # some county COUNTY some office (as for judges)
#             county = head
#             office = tail
    
### Use this if Circuit Court Branch is a district
## Next line enabled to remove Branch from office, to match current output files
    office, sep, tail = office.partition(',')
#     if tail:
#         district = tail.strip()
#         district = tail.split()[-1].strip()       # branch number
    
    # Separate party from office, handle district after '-'
### postpone this improvement to pass tests
#     office, sep, tail = office.partition('-')
#     tail = tail.strip()
### postpone this improvement to pass tests
#     if tail:
#         if tail.isdigit():
#             district = tail
#         else:
#             party = tail
    
    office = office.strip()
    party = party.replace(' PARTY', '')
    return office, county, district, party


def parse_sheet(sheet, office):
#     office, office_county, district, party = parse_office(office)
    parse = parse_office(office)
#     print '{:65} {}'.format(office, parse)
    office, office_county, district, party = parse
    candidates, parties, start_row = detect_headers(sheet)
    output = []
    for i in range(start_row, sheet.nrows):
        results = sheet.row_values(i)
        if "Totals" in results[1]:
            continue
        
        col0 = results[0].strip()
        if col0 != '':
            county = col0
        elif office_county != '':
            county = office_county
        
        ward = results[1].strip()
        
        total_votes = results[2]
        ### Doesn't clean_row() do this? (needs unicode check?)
        if isinstance(total_votes, six.string_types):
            total_votes = total_votes.replace(",","").strip()
            if total_votes.isdigit():
                total_votes = int(total_votes)
        
        # Some columns are randomly empty.
        candidate_votes = results[3:]
        for index, candidate in enumerate(candidates):
            if (candidate == None or candidate == ''):
                continue
            else:
                party = parties[index]
                output.append([county, ward, office, district, total_votes, 
                                party, candidate, candidate_votes[index]])
    return output


def parse_without_title_sheet(sheet, office):
    """ Return list of records for (string) office, extracted from xlrd sheet. """
    output = []
    candidates, parties, start_row = detect_headers(sheet)
    if '' in candidates:
        del candidates[candidates.index(''):]   # truncate at first empty cell
    district = ''
    party = ''
    county = ''
    for rowx in range(start_row, sheet.nrows):
        row = sheet.row_values(rowx)
        if "Totals" in row[0] or "Totals" in row[1]:
            continue
        col0 = row[0].strip()
        if col0 != '':
            county = col0
        ward = row[1].strip()
        total_votes = row[2]
        if isinstance(total_votes, six.string_types):
            total_votes = total_votes.replace(",","").strip()
            if total_votes.isdigit():
                total_votes = int(total_votes)
        candidate_votes = row[3:]
        for index, candidate in enumerate(candidates):
            output.append([county, ward, office, district, total_votes, party, candidate,
                            candidate_votes[index]])
    return output

def get_all_results(ids, url, process_function=process_local):
  r = requests.get(url)
  if r.status_code == 200:
    parsed = json.loads(r.content)['objects']
    for id in ids:
      print "id %s" % id
      for election in parsed:
        if election['id'] == id:
          get_election_result(election, process_function)


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
446,664,422,443,
444,                    # contains both xls and pdf files
445,447]

zip_file = [437]

# No title sheet, older format, repeated headings
xls_2002_to_2010_not_tested = [
426,427,428,429,
430,431,432,433,434,435,436,
438,439,440,441,
444,410]                    # contains both xls and pdf files


# Working Elections!

# Has a sheet with no cover sheet unlike others.
no_title_sheet = [421]

xls_2002_to_2010_working = [1577,1578,442]

working = [
404,405,407,408,
409,411,413,415,416,
419,
421,            # no title sheet
424,425,
1539,1573,1574,1575,1576,
1658,1659,1660,1661,1662
]

# Files with offices in second column of title sheet:
#   1573,1574,1576,1658,1659,1660,1661

small_test_set = [404, 407, 408, 419, 1659, 1573, 1574, 1575, 1576, 1661, 1662]

### use process_offices_test to view office string formats
# get_all_results(small_test_set, WIOpenElectionsAPI, process_offices_test)
# get_all_results(small_test_set, WIOpenElectionsAPI)

get_all_results(working, WIOpenElectionsAPI)

get_all_results(xls_2002_to_2010_working, WIOpenElectionsAPI, process_local_xls_2002_to_2010)
