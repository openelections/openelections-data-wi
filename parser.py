# -*- coding: utf-8 -*-

import json
import os
import sys

import requests
import six
import unicodecsv as csv
import xlrd

import cleaner

### Is this needed?
reload(sys)
sys.setdefaultencoding('utf8')


headers = ["county","ward","office","district","total votes","party","candidate","votes"]

offices_without_title_sheet = ['JUSTICE OF THE SUPREME COURT']

# {colA_header: num_missing} -- given first header, number of missing columns
#   (for 2002 to 2010 single sheet spreadsheets)
first_header = {'ELECTION': 0, 'OFFICE TYPE': 3, 'COUNTY': 10}


def collect_columns(row, start_col):
    """Collect data from row starting at start_col, until empty or bad cell."""
    data = []
    for value in row[start_col:]:
        if value in ('', 'dem'):
            break
        data.append(value)
    return data


def process_xls_2002_to_2010(sheet):
    """Return list of records from spreadsheet in 2002-2010 format"""
    results = []
    for rowx in range(sheet.nrows):     # index to rows
        row = sheet.row_values(rowx)
        colA = row[0]
        if colA in first_header:
            # first row of block, collect candidate names
            col_offset =  first_header[colA]
            candidate_col = 17 - col_offset         # first column of candidate data
            candidates = collect_columns(row, candidate_col)
            continue
        elif colA in ('DATE', 'KEYWORD', 'NAME'):
            # second row of block, collect party names
            parties = collect_columns(row, candidate_col)
            for i in range(len(candidates) - len(parties)):
                parties.append('')
            continue
        elif colA in ('', ' '):
            continue
        
        # not header nor blank: assume this is a data row
        office_col = 4 - col_offset
        if office_col >= 0:
            office, _, district = row[office_col].partition(',')
            if district.strip():    # some non-space characters
                district = district.rsplit(None, 1)[-1]
        else:
            # (use last office)
            district = ''
        county = row[10 - col_offset]
        ward_info = [row[col - col_offset] for col in (11, 13, 16)]
        ward = '{} of {} {}'.format(*ward_info)
        
        votes = collect_columns(row, candidate_col)
        if isinstance(votes[0], basestring) and not votes[0].isdigit():
            print '    row {}, col {}, data:"{}"'.format(rowx, candidate_col, votes[0])
            raise ValueError('Non-digit chars in votes field')
        # assume votes are strings of digits, or ints or floats
        votes = map(int, votes)
        total_votes = sum(votes)
        
        for i, candidate in enumerate(candidates):
            results.append([
                county, ward, office, district, total_votes, parties[i], candidate, votes[i]
            ])
    return results


def get_offices(sheet):
    """Extract office names from title sheet.
    Return list of names and index of first sheet to process.
    """
    # Title page may have offices in column A or B (0 or 1), detect which column
    column = 0 if sheet.cell_value(1, 0) else 1
    offices = sheet.col_values(column)[1:]     # skip first row
    if offices[0] == '':
        # first office empty, assume first sheet is not a title sheet
        offices = []
        sheet_index = 0     # start with sheet 0
        for office in offices_without_title_sheet:
            # Look for an office in first column, search first 12 rows
            if office in sheet.col_values(colx=0, start_rowx=0, end_rowx=12):
                offices.append(office)
                break
    else:
        sheet_index = 1     # start with sheet 1
    return offices, sheet_index


def process(filename):
    try:
        xlsfile = xlrd.open_workbook(filename)
    except IOError as exc:
        print 'Failed to open input file {}'.format(filename)
        print exc
        print
        return []
    sheet = xlsfile.sheet_by_index(0)
    results = []
    if sheet.cell_value(rowx=0, colx=0) in first_header:
        results.append(process_xls_2002_to_2010(sheet))
    else:
        offices, sheet_index = get_offices(sheet)
        for office in offices:
            sheet = xlsfile.sheet_by_index(sheet_index)
            results.append(parse_sheet(sheet, office, sheet_index))
            sheet_index += 1
    return results


def make_filepath(election):
    type = election['race_type']
    if election['special']:
        type = 'special_' + type
    start_date = election['start_date'].replace("-","")
    filename = '{}__wi__{}_ward.csv'.format(start_date, type)
    print 'Processing ' + filename
    year = start_date[:4]
    if not os.path.isdir(year):
        os.mkdir(year)
    filepath = os.path.join(year, filename)
    return filepath


def get_election_result(election):
    filepath = make_filepath(election)
    outfile = open(filepath, 'w')
    wr = csv.writer(outfile)
    wr.writerow(headers)
    direct_links = election['direct_links']
    for direct_link in direct_links:
        infilename = os.path.basename(direct_link)
        cached_filename = os.path.join('local_data_cache', 'data', infilename)
        if cached_filename.lower().endswith('.pdf'):
            print '**** Skipping PDF file: ' + cached_filename
            continue
        print 'Opening ' + cached_filename
        results = process(cached_filename)
        for result in results:
            for row in result:
                row = cleaner.clean_particular(election, row)
                row = cleaner.clean_row(row)
                if "Office Totals:" not in row:
                    wr.writerow(row)


def open_file(url, filename):
    r = requests.get(url)
    if r.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(r.content)
    xlsfile = xlrd.open_workbook(filename)
    return xlsfile


def any_party_in(sequence):
    """ Return True if any party abbreviation is an element of sequence, else False.
        Uses abbreviations from cleaner.party_recode map.
    """
    for party in cleaner.party_recode.values():
        if party in sequence:
            return True
    return False


CAND_COL = 3    # column holding first candidate
TOTAL_VOTES_HEADER = 'Total Votes Cast'

def detect_headers(sheet):
    """ Extract candidate names and parties from sheet.
    
        Returns: candidates, parties, start_row
    """
    # Search rows for Total Votes header, in column before candidates
    for rowx in range(3, 12):
        value = sheet.cell_value(rowx, CAND_COL - 1)
        if value.strip() == TOTAL_VOTES_HEADER:
            break
    else:   # loop not exited with break
        raise Exception('"{}" header not found'.format(TOTAL_VOTES_HEADER))
    
    row = sheet.row_values(rowx, start_colx=CAND_COL)
    if any_party_in(row):   # look for any party abbreviation in row
        parties = row
        candidates = sheet.row_values(rowx + 1, start_colx=CAND_COL)
        start_row = rowx + 2
    else:   # assume parties in previous row
        parties = sheet.row_values(rowx - 1, start_colx=CAND_COL)
        candidates = row
        start_row = rowx + 1
    return candidates, parties, start_row


def parse_office(office_string):
    """ Parse office string, returning (office, district, party)
        
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
        district = ''
        party = ''
    
    # Separate party from office, handle district after '-'
    head, sep, tail = office.partition('-')
    tail = tail.strip()
    if tail:
        if tail.isdigit():
            office = head
            district = tail
        elif head.endswith(' '):    # not a hyphenated name
            office = head
            party = tail
    
    office = office.strip()
    party = party.replace(' PARTY', '')
    return office, district, party


def parse_sheet(sheet, office, sheet_index):
    """Return list of records for (string) office, extracted from xlrd sheet."""
    office, district, party = parse_office(office)
    candidates, parties, start_row = detect_headers(sheet)
    if sheet_index == 0 and '' in candidates:
        del candidates[candidates.index(''):]   # truncate at first empty cell
        ### TO DO: Process recount results after first empty cell
    county = ''
    output = []
    for rowx in range(start_row, sheet.nrows):
        row = sheet.row_values(rowx)
        if "Totals" in row[0] or "Totals" in row[1]:
            continue
        col0 = row[0].strip()
        if col0 != '':
            county = col0
        ward = row[1].strip()
        total_votes = row[2]
        candidate_votes = row[CAND_COL:]
        for index, candidate in enumerate(candidates):
            if candidate:   # column not empty
                party = parties[index]
                output.append([county, ward, office, district, total_votes, 
                                party, candidate, candidate_votes[index]])
    return output


def get_all_results(ids, url):
  r = requests.get(url)
  if r.status_code == 200:
    parsed = json.loads(r.content)['objects']
    for id in ids:
      print "id %s" % id
      for election in parsed:
        if election['id'] == id:
          get_election_result(election)


def get_result_for_json(filename):
    with open(filename) as jsonfile:
        election = json.load(jsonfile)
        get_election_result(election)


WIOpenElectionsAPI = "http://openelections.net/api/v1/election/?format=json&limit=0&state__postal=WI"


# All ids from available elections.
available_ids = [
1658,1659,1660,1661,
1576,1573,1574,1575,
1538,1539,
404,405,
407,408,409,410,411,
1662,
413,415,416,419,421,422,424,425,426,427,428,429,430,
431,432,433,434,435,436,437,438,439,440,441,442,443,444,445,446,447,448,
664,
674,685,689,
1577,1578]

# Elections with no files available.
no_results_ids = [674, 685, 689,448]

# File 440 won't open in Pages, but parses fine (Google docs also works)

# Election with PDF files.
pdf_elections = [
    422, 443,
    444,                # contains both xls and pdf files
    445, 446, 447, 
    664,
    1711
]

zip_file = [437]


# Working Elections:

# Single sheet spreadsheets, older format, repeated headings
xls_2002_to_2010_working = [
    426, 427, 428, 429, 
    430, 431, 432, 433, 434, 435, 436,
    438, 439, 440, 441, 442, 
    1577, 1578
]
xls_2002_to_2010_unfinished = [444]     # contains both xls and pdf files

xls_after_2010_working = [
    404,405,407,408,409,410,411,
    413,415,416,419,
    421,                        # Single sheet with no cover sheet, unlike others
    424,#425, not working yet!
    1538,1539,1573,1574,1575,1576,
    1658,1659,1660,1661,1662,
    1748,1710
]

# Files with offices in second column of title sheet (working):
#   1573,1574,1576,1658,1659,1660,1661

working = xls_2002_to_2010_working + xls_2002_to_2010_unfinished
working += xls_after_2010_working

test_set = [
404, 407, 408, 419, 
426, 434, 440, 444,
1573, 1574, 1575, 1576, 1577, 1659, 1661, 1662
]
# get_all_results(test_set, WIOpenElectionsAPI)

# jsonfilenames = ['1748.json', '1710.json']
# for filename in jsonfilenames:
#     get_result_for_json(filename)


get_all_results(working, WIOpenElectionsAPI)

