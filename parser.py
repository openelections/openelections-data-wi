# -*- coding: utf-8 -*-

import json
import os
import sys

import csv
import xlrd
import zipfile

import cleaner
import fetch
import officetable


output_headers = ["county", "ward", "office", "district", "total votes",
                    "party", "candidate", "votes"]


first_header = {'ELECTION': 0, 'OFFICE TYPE': 3, 'COUNTY': 10,
                    'ELECTION DATE': 0}
"""Given first header, number of missing columns
        {colA_header: num_missing}
        (for year 2000 to 2010 single sheet spreadsheets)
"""


warnings = {
    'pdf_skipped': False,     # print(warning when skipping a PDF input file
}


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
            col_offset =  first_header[colA]    # number of missing columns
            if col_offset > 0:
                print("Note: section at row {} is missing {} columns".format(
                    rowx + 1, col_offset))
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
            office_table.add_office(office)
        else:
            # Office column is missing from data
            #   This occurs for district 14 data in
            #   Libertarian_2008_FallElection_StateSenator_WardbyWard.xls
            #   (Not seen in any other file so far)
            # Use previous office name
            district = '14'     # kludge to handle this special case
        county = row[10 - col_offset]
        ward_info = [row[col - col_offset] for col in (11, 13, 16)]
        ward = '{} of {} {}'.format(*ward_info)

        votes = collect_columns(row, candidate_col)
        if isinstance(votes[0], basestring) and not votes[0].isdigit():
            print('   row {}, col {}, data:"{}"'.format(
                rowx, candidate_col, votes[0]))
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
        print(fieldname, 'not found in spreadsheet column headers:')
        print(col_headers)
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
        office_table.add_office(office)

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
        print('Failed to open input file {}'.format(filename))
        print(exc)
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
    print('Processing ' + filename)
    year = start_date[:4]
    if not os.path.isdir(year):
        os.mkdir(year)
    filepath = os.path.join(year, filename)
    return filepath


def get_election_result(election, no_output=False):
    filepath = make_filepath(election)
    if not no_output:
        outfile = open(filepath, 'wt')
        wr = csv.writer(outfile)
        wr.writerow(output_headers)
    office_table.new_election()
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
                if "Office Totals:" not in row and not no_output:
                    wr.writerow(row)
    if row is None and not no_output:   # no rows written, delete file
        outfile.close()
        os.remove(filepath)
        print('No data parsed, output file removed')
    office_table.tabulate_offices(election)


def process_file(cached_filename, election):
    if cached_filename.lower().endswith('.pdf'):
        if warnings['pdf_skipped']:
            print('**** Skipping PDF file: ' + cached_filename)
        return []
    elif cached_filename.lower().endswith('.zip'):
        archive = zipfile.ZipFile(cached_filename, 'r')
        archive.extractall('tmp/')
        archive.close()
        results = []
        # sort os.listdir() output because order differs on Linux vs MacOS
        for filename in sorted(os.listdir('tmp/')):
            local_file = 'tmp/' + filename
            results = results + process_file(local_file, election)
            os.remove(local_file)
        return results
    else: # Excel file
        print('Opening ' + cached_filename)
        return process(cached_filename, election)


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
            print('##### Warning: SCATTERING missing in sheet {} "{}"'.format(
                    sheet_index, sheet.name))

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
          RECALL STATE SENATE-21 - DEMOCRATIC
          STATE SENATOR DISTRICT 1-Democratic
    """
    office = office_string.upper()
    office = office.replace(u'\u2015','-')   # change HORIZONTAL BAR to hyphen
    office = office.replace(u'\u2013', '-')  # change EN DASH to hyphen

    if ' DISTRICT ' in office and ' DISTRICT ATTORNEY' not in office:
        head, sep, tail = office.partition(' DISTRICT ')
        office = head.strip(',- ')
        district, sep, party = tail.partition(' ')
        district, _, pty = district.partition('-')  # handle "1-<party>"
        party = pty + sep + party
        party = party.strip('- ')
    else:
        district = ''
        party = ''

    # Handle D.A. followed by county, or remove party
    head, sep, tail = office.partition(' -')
    tail = tail.strip()
    if tail:
        if tail.endswith(' COUNTY'):        # id 409, 2012-11-06 D.A.
            head = head.strip()
            assert head == 'DISTRICT ATTORNEY'
            office = tail + ' ' + head      # ____ County District Attorney
        else:
            office = head
            party = tail

    # Handle district after '-'
    head, sep, tail = office.partition('-')
    tail = tail.strip()
    if tail.isdigit():
        office = head
        district = tail

    office = office.strip()
    party = party.replace(' PARTY', '')
    party = party.strip('0123456789-')      # remove years appended to office

    office_table.add_office(office)
    return office, district, party


def parse_sheet(sheet, office, sheet_index, election):
    """Return list of records for (string) office, extracted from spreadsheet.
        This is used to parse Fall 2010 and later elections.
    """
    office_was = office
    office, district, party = parse_office(office)
    if party and election['race_type'] == 'general':
        print('##### Warning: skipping sheet "{}"'.format(sheet.name)),
        print('in general election')
        print( '    Party in office name indicates primary:', office_was)
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


def get_all_results(ids, no_output=False):
    """Process results for election ids given;
        if none given, process all ids in metadata.
    """
    metadata = fetch.read_cached_metadata()
    for election in metadata['objects']:
        if ids and election.get('id') not in ids:
            continue    # filter by ids list if not empty
        print('id {id}'.format(**election))
        get_election_result(election, no_output)


def get_result_for_json(filename):
    with open(filename) as jsonfile:
        election = json.load(jsonfile)
        get_election_result(election)


# API url: for debugging, metadata is now read from cached file
# http://openelections.net/api/v1/election/?format=json&limit=0&state__postal=WI


"""
Elections with no files available:
    448, 664, 674, 689

Election results available only in PDF files:
    437 (2006-09-12) PDF and excel in zip files, some offices only PDF
    444 (2004-11-02) has xls files for President and Senate,
        only PDFs for House, State Senate, State Assembly, District Attorney
    443, 445, 446, 447,
    685, 1756

Single sheet spreadsheets, 2002-2010 format, two-line repeated headings:
    426-442, 1577, 1578 ...

Single sheet spreadsheets, 2002-2010 format, single-line heading:
    1845 (2000-11-07), 2 of 6 xls files have this format

2011-04-05 general election (id 421) Supreme Court xls has a
    single sheet with no title sheet
        WARD_BY_WARD_FOR_SPRING_2011_ELECTION_AND_RECOUNT.xls

xls files with offices in second column of title sheet:
    1573, 1574, 1576, 1658, 1659, 1660, 1661
"""


if __name__ == '__main__':
    usage_msg = """Usage: {} [-n] <list of ids>]
       Parse input files and process results for listed ids.
       Omit ids to process all ids for state.
       Use option -n for no results output.
       Uses elections metadata from file "{}".
    """.format(sys.argv[0], fetch.metadata_filepath)
    args = sys.argv[1:]
    no_output = (args[:1] == ['-n'])
    if no_output:
        args = args[1:]
    if not all(map(str.isdigit, args)):
        print(usage_msg)
        print('Args must be positive integers (election ids)')
    else:
        office_table = officetable.OfficeTable()
        ids = map(int, args)
        get_all_results(ids, no_output=no_output)
        office_table.print_summary()
