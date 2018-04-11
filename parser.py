# -*- coding: utf-8 -*-

import json
import os
import sys

import requests
import unicodecsv as csv
import xlrd
import zipfile

import cleaner


output_headers = ["county", "ward", "office", "district", "total votes",
                    "party", "candidate", "votes"]


first_header = {'ELECTION': 0, 'OFFICE TYPE': 3, 'COUNTY': 10,
                    'ELECTION DATE': 0}
"""Given first header, number of missing columns
        {colA_header: num_missing}
        (for year 2000 to 2010 single sheet spreadsheets)
"""


def collect_columns(row, start_col):
    """Collect data from row starting at start_col, until empty or bad cell"""
    data = []
    for value in row[start_col:]:
        if value in ('', 'dem'):
            break
        data.append(value)
    return data


def split_candidate_party(candidates):
    """Split list of "<candidate> <party>" into separate lists"""
    parties = []
    for i, candidate in enumerate(candidates):
        if candidate == 'Scattering':
            parties.append('')
            continue
        for party in cleaner.party_recode:
            head, __, __ = candidate.rpartition(party)
            if head:    # party found in candidate field
                parties.append(party)
                candidates[i] = head
                break   # next candidate
        else:   # no break
            raise ValueError(
                'Party not found in candidate "{}"'.format(candidate))
    return candidates, parties


def process_xls_2000_to_2010(sheet):
    """Return list of records from spreadsheet in 2000-2010 formats"""
    results = []
    for rowx in range(sheet.nrows):     # index to rows
        row = sheet.row_values(rowx)
        colA = str(row[0]).strip()
        if colA in first_header:
            # first row of block, collect candidate names
            col_offset =  first_header[colA]
            candidate_col = 17 - col_offset   # first column of candidate data
            candidates = collect_columns(row, candidate_col)
            if colA == 'ELECTION DATE':       # single header, extract parties
                candidates, parties = split_candidate_party(candidates)
            continue
        elif colA in ('DATE', 'KEYWORD', 'NAME'):
            # second row of block, collect party names
            parties = collect_columns(row, candidate_col)
            parties.extend([''] * (len(candidates) - len(parties)))
            continue
        elif colA in ('', 'SQL>') or colA.endswith('rows selected.'):
            continue    # not a data row
        
        # not header nor blank: assume this is a data row
        office_col = 4 - col_offset
        if office_col >= 0:
            office = row[office_col]
            head, _, district = office.partition(', District ')
            if district:        # separator was found
                office = head
                district = district.split()[-1]     # parse 'No. 1'
        else:
            # (use last office)
            district = ''
        county = row[10 - col_offset]
        ward_info = [row[col - col_offset] for col in (11, 13, 16)]
        ward = '{} of {} {}'.format(*ward_info)
        
        votes = collect_columns(row, candidate_col)
        if isinstance(votes[0], basestring) and not votes[0].isdigit():
            print '   row {}, col {}, data:"{}"'.format(
                rowx, candidate_col, votes[0])
            raise ValueError('Non-digit chars in votes field')
        # assume votes are strings of digits, or ints or floats
        votes = map(int, votes)
        total_votes = sum(votes)
        
        for i, candidate in enumerate(candidates):
            results.append([county, ward, office, district, total_votes,
                parties[i], candidate, votes[i]])
    return results


def process_xls_2012_DA_primary(sheet):     # election id 411
    """Return list of records from 2012-08-14 District Attorney spreadsheet"""
    
    fieldnames = ['ContestName', 'CountyName', 'CandidateName',
                    'ReportingUnitText', 'VoteCount']
    col_headers = sheet.row_values(rowx=0)  # first row
    try:
        # Find indexes of desired fields in spreadsheet
        fieldindexes = [col_headers.index(fieldname) 
                            for fieldname in fieldnames]
    except ValueError:
        print fieldname, 'not found in spreadsheet column headers:'
        print col_headers
        raise
    
    results = []
    candidate_votes = []
    previous_race_place = ()
    candidates = []
    for rowx in range(1, sheet.nrows):     # index to rows
        row = sheet.row_values(rowx)
        office, county, candidate, ward, votes = [
                                    row[col] for col in fieldindexes]
        # split office and party, reorder office
        parts = office.split(' - ')
        assert len(parts) == 3
        da, da_county, party = parts
        assert da == 'District Attorney'
        da_county = da_county.rstrip(' ')
        assert da_county.endswith(' County')
        office = da_county + ' ' + da       # ____ County District Attorney
        assert party in cleaner.party_recode.values()

        district = ''
        race_place = county, ward, office, district, party
        if previous_race_place and (race_place != previous_race_place):
            results.extend(collect_results(
                            candidates, candidate_votes, previous_race_place))
            candidates = []
            candidate_votes = []
        candidates.append(candidate)
        candidate_votes.append(votes)
        previous_race_place = race_place
    results.extend(collect_results(candidates, candidate_votes, race_place))
    return results

def collect_results(candidates, votes, race_place):
    results = []
    county, ward, office, district, party = race_place
    total_votes = sum(votes)
    for i, candidate in enumerate(candidates):
        results.append([county, ward, office, district, total_votes, party,
                        candidate, votes[i]])
    return results


def get_offices(sheet):
    """Extract office names from title sheet.
    Return list of names and index of first sheet to process.
    """
    # Determine file format by checking a few cells
    # (0-origin row and col numbers)
    row1_AB = sheet.row_values(rowx=1, start_colx=0, end_colx=2)
    value_2A = sheet.cell_value(rowx=2, colx=0) if sheet.nrows > 2 else ''
    
    if ''.join(row1_AB) == '':
        # First two cols in row 1 are blank,
        #   is this 2011-04-05 Supreme Court election (id 421)?
        office = 'JUSTICE OF THE SUPREME COURT'
        if value_2A == office:
            offices = [office]
            sheet_index = 0     # start parsing data with sheet 0
        else:
            raise Exception('Unrecognized spreadsheet format')
    else:
        if value_2A == 'Canvass Detail':   # probably 2010-09-14, id 425
            row = 3     # offices start in row 3 (0-origin)
            column = 0
        else:   # normal title sheet, offices in column A or B
            row = 1
            column = 1 if sheet.cell_value(rowx=1, colx=0) == '' else 0
        offices = sheet.col_values(colx=column, start_rowx=row)
        sheet_index = 1     # data starts on sheet 1
        
    return offices, sheet_index


def process(filename, election):
    try:
        xlsfile = xlrd.open_workbook(filename)
    except IOError as exc:
        print 'Failed to open input file {}'.format(filename)
        print exc
        print
        return []
    sheet0 = xlsfile.sheet_by_index(0)
    sheet0_cell0A = sheet0.cell_value(rowx=0, colx=0)   # 1st row, 1st column
    
    sheet1_cell0A = None
    if xlsfile.nsheets > 1:
        sheet1 = xlsfile.sheet_by_index(1)
        if sheet1.nrows > 0:
            sheet1_cell0A = sheet1.cell_value(rowx=0, colx=0)        
    results = []
    
    # Check for unusual file formats
    if sheet1_cell0A == 'ElectionName':
    	results.append(process_xls_2012_DA_primary(sheet1))
    # for an older-style header, process single sheet file
    elif sheet0_cell0A in first_header:
        results.append(process_xls_2000_to_2010(sheet0))
    
    else:
        offices, sheet_index = get_offices(sheet0)
        for office in offices:
            sheet = xlsfile.sheet_by_index(sheet_index)
            results.append(parse_sheet(sheet, office, sheet_index, election))
            sheet_index += 1
    return results


def make_filepath(election):
    # See http://docs.openelections.net/archive-standardization/
    start_date = election['start_date'].replace("-","")
    state = 'wi'
    party = ''
    special = 'special' if election['special'] else ''
    race_type = election['race_type']
    reporting_level = 'ward'
    names = [start_date, state, party, special, race_type, reporting_level]
    names = filter(bool, names)     # remove empty names
    filename = '__'.join(names) + '.csv'
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
    wr.writerow(output_headers)
    direct_links = election['direct_links']
    row = None
    for direct_link in direct_links:
        infilename = os.path.basename(direct_link)
        cached_filename = os.path.join('local_data_cache', 'data', infilename)
        results = process_file(cached_filename, election)
        for result in results:
            for row in result:
                row = cleaner.clean_particular(election, row)
                row = cleaner.clean_row(row)
                if "Office Totals:" not in row:
                    wr.writerow(row)
    if row is None:     # no rows written, delete file
        outfile.close()
        os.remove(filepath)
        print 'No data parsed, output file removed'


def process_file(cached_filename, election):
    if cached_filename.lower().endswith('.pdf'):
        print '**** Skipping PDF file: ' + cached_filename
        return []
    elif cached_filename.lower().endswith('.zip'):
        archive = zipfile.ZipFile(cached_filename, 'r')
        archive.extractall('tmp/')
        archive.close()
        results = []
        for filename in os.listdir('tmp/'):
            local_file = 'tmp/' + filename
            results = results + process_file(local_file, election)
            os.remove(local_file)
        return results
    else: # Excel file
        print 'Opening ' + cached_filename
        return process(cached_filename, election)


def open_file(url, filename):
    r = requests.get(url)
    if r.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(r.content)
    xlsfile = xlrd.open_workbook(filename)
    return xlsfile


CAND_COL = 3    # column holding first candidate
TOTAL_VOTES_HEADER = 'Total Votes Cast'

def extract_candidates(sheet, sheet_index):
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
    
    # Total Votes header in rowx, candidates in this row or next
    # Candidate row will have "SCATTERING" in it
    row = sheet.row_values(rowx, start_colx=CAND_COL)
    if "SCATTERING" in row:
        candidates = row
        parties = sheet.row_values(rowx - 1, start_colx=CAND_COL)
    else:
        parties = row
        rowx += 1
        candidates = sheet.row_values(rowx, start_colx=CAND_COL)
        if "SCATTERING" in candidates:
            # Fill in party if missing for "Scattering" candidate in primaries
            ### Check if election['race_type'] == 'primary'?
            scattering_index = candidates.index("SCATTERING")
            if parties[scattering_index] == '':
                office_title = sheet.cell_value(rowx - 3, 0)
                party = office_title.rpartition(' - ')[-1].strip().title()
                party = cleaner.party_recode.get(party)
                # assume a primary election if office ends in a party name
                if party:
                    parties[scattering_index] = party
        else:
            print 'Warning: SCATTERING missing, sheet {}'.format(sheet_index)
    
    start_row = rowx + 1        # first data row
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
    office = office_string.upper()
    office = office.replace(u'\u2015','-')   # change HORIZONTAL BAR to hyphen
    office = office.replace(u'\u2013', '-')  # change EN DASH to hyphen
    
    if ' DISTRICT ' in office and ' DISTRICT ATTORNEY' not in office:
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
        elif tail.endswith(' COUNTY'):      # id 409, 2012-11-06 D.A.
            head = head.strip()
            assert head == 'DISTRICT ATTORNEY'
            office = tail + ' ' + head      # ____ County District Attorney 
        elif head.endswith(' '):    # not a hyphenated name
            office = head
            party = tail
    
    office = office.strip()
    party = party.replace(' PARTY', '')
    party = party.strip('0123456789-')      # remove years appended to office
    return office, district, party


def parse_sheet(sheet, office, sheet_index, election):
    """Return list of records for (string) office, extracted from spreadsheet.
        This is used to parse Fall 2010 and later elections.
    """
    office, district, party = parse_office(office)
    if party and election['race_type'] == 'general':
        print '##### Warning: skipping sheet "{}"'.format(sheet.name),
        print 'in general election: party in office name indicates primary'
        print  '    {} (id {})'.format(election['end_date'], election['id']),
        print office, district, party
        return []
    candidates, parties, start_row = extract_candidates(sheet, sheet_index)
    offset = 0
    if sheet_index == 0 and '' in candidates:
        # probably this is 2011-04-05 Supreme Court election (id 421)
        i = candidates.index('') + 1    # next after blank
        if len(candidates) > i and candidates[i] == TOTAL_VOTES_HEADER:
            # this is the second total votes header, for recounts
            offset = i + 1          # column offset to get recount data
            candidates = candidates[offset:]
            parties = parties[offset:]
    cand_col = CAND_COL + offset    # 1st candidate is in this column
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
        total_votes = row[2 + offset]
        candidate_votes = row[cand_col:]
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

# http://openelections.net/api/v1/election/?format=json&limit=0&state__postal=WI
WIOpenElectionsAPI = "http://openelections.net/api/v1/election/"
WIOpenElectionsAPI += "?format=json&limit=0&state__postal=WI"


# Elections with no files available.
no_results_ids = [448, 664, 674, 689]


# Working Elections:

# Single sheet spreadsheets, older format, repeated headings
xls_2002_to_2010_working = [
    426, 427, 428, 429, 
    430, 431, 432, 433, 434, 435, 436, 437,
    438, 439, 440, 441, 442, 
    1577, 1578
]
xls_2002_to_2010_unfinished = [444]     # contains both xls and pdf files

xls_2010_onward_working = [
    404,405,407,408,409,
    410,411,413,415,416,419,
    421,                    # Single sheet with no cover sheet, unlike others
    422,
    424,425,
    1538,1539,1573,1574,1575,1576,
    1658,1659,1660,1661,1662,
    1710,1711,1748,1755,1761
]

# Files with offices in second column of title sheet (working):
#   1573,1574,1576,1658,1659,1660,1661

working = xls_2002_to_2010_working + xls_2002_to_2010_unfinished
working += xls_2010_onward_working
working += range(1822,1852) + [1864, 1865]


# Running from command line without args, process results for all working ids.
# With args, get results for the ids listed as args.
if __name__ == '__main__':
    args = sys.argv[1:]
    if args:
        if all(map(str.isdigit, args)):
            ids = map(int, args)
        else:
            print 'Args must be positive integers (election ids)'
            sys.exit(1)
    else:
        ids = working
    get_all_results(ids, WIOpenElectionsAPI)


