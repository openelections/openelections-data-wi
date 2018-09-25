# Convert our "feature tests" format to csv and back
# David "Davi" Post, 2018-05-23
# for OpenElections project in WI

from __future__ import unicode_literals

import sys
import StringIO

import unicodecsv as csv


feature_file_header = """
Feature: WI Elections

  Scenario Outline: Tests
    When I visit the election file
    And I search for <party> party candidate <candidate> running for <office> <district> in the <ward> in <county>
    Then I should see <votes> out of <total>

""".lstrip()

examples_prefix = '  Examples: '
fieldnames = ('filename,party,candidate,county,office,district,' +
                'ward,votes,total').split(',')
feature_file_delimiter = '|'

indent = 4 * ' ' + feature_file_delimiter

# Widths of columns for feature tests
widths_normal =     [40, 12, 44, 12, 48, 8, 8]  # for fieldname[2] ...
widths_party =   [8, 32, 12, 44, 12, 48, 8, 8]  # add party column
widths_long_ward =  [36, 12, 18, 12, 78, 8, 8]  # for long ward names
widths_med_ward =   [24, 12, 40, 12, 68, 8, 8]  # for medium-long ward


def get_widths(line, sep=feature_file_delimiter):
    """Find widths of columns (separated by sep) in line"""
    cols = [i for i, char in enumerate(line) if char == sep]
    widths = [cols[i + 1] - cols[i] for i in range(len(cols) - 1)]
    widths = [cols[0] + 1] + widths
    return widths


def feature2csv(line, sep=feature_file_delimiter):
    parts = csv.reader([line], delimiter=sep).next()
    parts = map(unicode.strip, parts)[1:-1]
    csv_buffer = StringIO.StringIO()
    writer = csv.writer(csv_buffer)
    writer.writerow(parts)
    return csv_buffer.getvalue()


def csv2feature(csv_line, ww=False):
    parts = csv.reader([csv_line]).next()
    col_widths = (widths_party if len(parts) == len(widths_party)
                               else widths_normal)
    if len(parts[-3]) >= col_widths[-3] or ww:      # use wide ward field
        col_widths = widths_long_ward
    return expand(parts, col_widths)


def expand(data, col_widths):
    """Format data list as string, adjusting col_widths as needed"""
    widths = col_widths[:]      # make a copy
    diffs = [len(data[i]) + 2 - width 
            for i, width in enumerate(widths)]
    for i, diff in enumerate(diffs[:-1]):
        if diff > 0 and diffs[i + 1] < 0:   # col i too wide, i+1 has room
            shrinkage = max(diffs[i + 1], - diff)
            widths[i + 1] += shrinkage
            diffs[i + 1] -= shrinkage
    field_format = ' {:<{width}}' + feature_file_delimiter
    parts = [field_format.format(field, width=widths[i] - 2)
                for i, field in enumerate(data)]
    return indent + ''.join(parts) + '\n'


def parse_feature_tests(feature_filepath, csv_filepath=None):
    """Read feature tests, write csv data"""
    testfile = open(feature_filepath)
    if csv_filepath is None:
        csv_filepath = feature_filepath + '.csv'
    csvfile = open(csv_filepath, 'w')
    writer = csv.writer(csvfile)
    writer.writerow(fieldnames)
    csv_delimiter = str(feature_file_delimiter)   # needs str, not unicode
    
    while True:
        for line in testfile:
            _, _, filename = line.partition(examples_prefix)
            if filename:    # prefix found
                break
        else:  # no break, end of file
            break
        row = [''] * len(fieldnames)
        row[0] = filename.rstrip()
        writer.writerow(row)
        
        testfile.next()     # skip fieldnames row
        for line in testfile:
            if not line.strip():
                break   # blank line, end of tests for current filename
            row = csv.reader([line], delimiter=csv_delimiter).next()
            row = map(unicode.strip, row)[:-1]
            if len(row) < len(fieldnames):    # party missing
                row.insert(0, '')
            writer.writerow(row)
        else:  # no break, end of file
            break


def format_feature_tests(csv_filepath):
    """Read csv data, write formatted feature tests"""
    csvfile = open(csv_filepath)
    reader = csv.reader(csvfile)
    feature_filepath = csv_filepath.replace('.csv', '')
    feature_file = open(feature_filepath, 'w')
    feature_file.write(feature_file_header)
    reader.next()       # discard header
    done = False
    col_widths = []
    data = []
    row = reader.next()
    try:
        while not done:
            filename = row[0]
            feature_file.write(examples_prefix + filename + '\n')
            rows = []
            for row in reader:
                if row[0]:      # next filename
                    break
                rows.append(row)
            else:   # no break, end of file
                done = True
            col_widths = fit_column_widths(rows)
            first_col = len(rows[0]) - len(col_widths)
            data = fieldnames[first_col:]   # section heading
            feature_file.write(expand(data, col_widths))
            for row_ in rows:
                data = row_[first_col:]
                line = expand(data, col_widths)
                feature_file.write(line.encode('utf8'))
            feature_file.write('\n')
    except StandardError as exc:
        print '*** Error formatting data: {}'.format(data)
        print '    using widths: {}'.format(col_widths)
        print '    in test for {}'.format(filename)
        raise


def fit_column_widths(rows):
    """Return best list of column widths for rows of data"""
    if rows[0][1]:         # if party column used
        col_widths = widths_party
    else:
        col_widths = widths_normal      # default
        cand_col = fieldnames.index('candidate')
        maxwidths = max_widths(rows)[cand_col:]
        ward_col = fieldnames.index('ward') - cand_col
        cand_col = 0
        if maxwidths[ward_col] >= widths_normal[ward_col]:
            col_widths = widths_long_ward
            if (maxwidths[ward_col] < widths_med_ward[ward_col]
                and maxwidths[cand_col] < widths_med_ward[cand_col]):
                col_widths = widths_med_ward    # better fit for long office
    return col_widths


def max_widths(rows):
    """Return maximum width for each column in a set of rows"""
    num_cols = len(rows[0])
    for row in rows[1:]:
        if len(row) != num_cols:
            raise ValueError(
                'Inconsistent row length\n  row = {}'.format(row))
    return [ max([len(row[col]) for row in rows])
            for col in range(num_cols) ]


feature_examples = [
"    | candidate                     | county        | office                                        | ward                                          | votes | total |",
"    | party | candidate                     | county        | office                                | ward                                          | votes | total |",
"    | DEM   | Mario R. Hall         | Milwaukee     | State Assembly                                | City Of Wauwatosa Ward 24                     | 7     | 104   |", 
"    | IND   | Peter Miguel Camejo & Ralph Nader | Brown     | President                         | VILLAGE OF HOWARD Wards 1 - 8                     | 27    | 3767  |",
"    | AME   | Scattering            | Menominee     | Menominee-Shawano County District Attorney    | TOWN OF MENOMINEE Ward 2                      | 0     | 0     |",
"    | Darrell L. Castle & Scott N. Bradley  | Burnett       | President                             | TOWN OF WOOD RIVER Ward 1-3                   | 10    | 517   |",
"    | Karen L. Seifert                  | Winnebago | Winnebago County Circuit Court, Branch 4  | VILLAGE OF WINNECONNE Wards 1 - 4                 | 91    | 128   |",
"    | David T. Prosser, Jr.         | Manitowoc     | Supreme Court             | CITY OF MANITOWOC Wards 17, 18, 22, 24 - 26, 28 - 30, 32, 34 & 36 | 306   | 555   |",
"    | Richard J. Spanbauer            | Fond Du Lac | State Assembly            | CITY OF FOND DU LAC Ward 39                                       | 0     | 0     |"
]


def run_examples():
    for line in feature_examples:
        csv_line = feature2csv(line)
        feature_line = csv2feature(csv_line)
        assert feature2csv(feature_line) == csv_line
        print feature_line,
    print


default_filepath = 'tests/features/wi-elections.feature'

if __name__ == '__main__':
    filepath = default_filepath
    if sys.argv[1:]:
        filepath = sys.argv[1]
    if filepath.endswith('.csv'):
        format_feature_tests(filepath)
    elif filepath.endswith('.feature'):
        parse_feature_tests(filepath)
    else:
        print """\nUsage: {} [filepath]\n
  For filepath suffix .csv, write feature test format to path without .csv
  For filepath suffix .feature, write csv data to path with added suffix .csv
  Without filepath, default to {}\n""".format(sys.argv[0], default_filepath)


