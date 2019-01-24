"""
run_spot_tests.py
Check for example records in CSV results files output by parser
David "Davi" Post, 2019-01
for OpenElections project in WI
"""

import io
import sys
import time

import unicodecsv as csv

import parser


default_tests_filepath = 'tests/features/wi-elections.feature.csv'


"""
Fields in results files:
    county,ward,office,district,total votes,party,candidate,votes
    (parser.output_headers)

Fields in tests file (wi-elections.feature.csv):
    filename,party,candidate,county,office,district,ward,votes,total

Results files are typically ordered by:
    office, district, county, ward
    (party and candidate not usually ordered)
"""


def test_result_file(filename, tests, party_indices):
    """Check that records in tests appear exactly once in named file.
        tests is a list of tests, each a record formatted like result data.
        party_indices gives start of missing party for each test, or -1
    """
    print 'Testing', filename
    year = filename[:4]
    assert year.isdigit()
    filepath = year + '/' + filename
    
    with io.open(filepath, encoding='utf-8') as results_file:
        test_counts = [0] * len(tests)   # number of times test data found
        results_file.next()     # skip header
        for record in results_file:
            for i, test in enumerate(tests):
                record_ = record
                pi = party_indices[i]
                if pi >= 0:   # party missing from test
                    if record[pi - 1:pi] == ',':
                        ci = record.find(',', pi)
                        datum = record[pi:ci]
                        if datum.isalpha() and datum.isupper():
                            # party in record, remove it (don't test)
                            record_ = record[:pi] + record[ci:]
                if record_ == test:
                    test_counts[i] += 1
    
    # Summarize errors
    num_errors = 0
    for i, test in enumerate(tests):
        count = test_counts[i]
        if count != 1:    # error if test data does not appear exactly once
            if count == 0:
                print '  Not found:',
            else:   # count > 1
                print '  Found {} times:'.format(count),
            print test
            num_errors += 1
    return num_errors


def run_tests(tests_filepath):
    """Read tests for each results file, check for specified records"""
    tests_file = open(tests_filepath)
    tests_reader = csv.DictReader(tests_file)
    # Get results fields, renaming "total votes" to "total"
    results_fields = [field.split()[0] for field in parser.output_headers]
    num_files = 0
    num_errors = 0
    num_tests = 0
    missing_party_marker = u'*p*'
    done = False
    row = tests_reader.next()
    while not done:
        filename = row['filename']
        tests = []          # list of test strings, data in results order
        party_indices = []  # index of missing party in test, or -1
        for row in tests_reader:
            if row['filename']:     # next file to test
                break
            for field in ('office', 'county', 'ward', 'candidate'):
                row[field] = row[field].title()
                if ',' in row[field]:
                    row[field] = '"' + row[field] + '"'
            if row['party'] == '':
                row['party'] = missing_party_marker
            # format test data as string, in results order
            test_data = ','.join([row[field] for field in results_fields])
            party_indices.append(test_data.find(missing_party_marker))
            test_data = test_data.replace(missing_party_marker, '')
            tests.append(test_data + '\n')
            
        else:   # no break, end of file
            done = True
        
        num_errors += test_result_file(filename, tests, party_indices)
        num_files += 1
        num_tests += len(tests)
    print
    print '{} files tested, {} tests, {} failed'.format(
            num_files, num_tests, num_errors)


if __name__ == '__main__':
    start = time.time()
    if len(sys.argv) > 2 or sys.argv[-1].startswith('-'):
        print '\nUsage: {} [<tests_filepath>]\n'.format(sys.argv[0])
    else:
        tests_filepath = default_tests_filepath
        if len(sys.argv) == 2:
            tests_filepath = sys.argv[1]
        run_tests(tests_filepath)
        print 'Elapsed time: {:.1f} seconds\n'.format(time.time() - start)

