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


default_tests_filepath = 'tests/wi-elections.tests.csv'


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


def test_result_file(filename, tests):
    """Check that records in tests appear exactly once in named file.
        tests is a list of tests, each a record formatted like result data.
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
                if record == test:
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
    done = False
    row = tests_reader.next()
    while not done:
        filename = row['filename']
        tests = []          # list of test strings, data in results order
        for row in tests_reader:
            if row['filename']:     # next file to test
                break
            row['ward'] = row['ward'].title()
            for field in ('office', 'county', 'ward', 'candidate'):
                if ',' in row[field]:
                    row[field] = '"' + row[field] + '"'
            # format test data as string, in results order
            test_data = ','.join([row[field] for field in results_fields])
            tests.append(test_data + '\n')
        else:   # no break, end of file
            done = True
        
        num_errors += test_result_file(filename, tests)
        num_files += 1
        num_tests += len(tests)
    print
    print '{} files tested, {} tests, {} failed'.format(
            num_files, num_tests, num_errors)
    return num_errors


if __name__ == '__main__':
    start = time.time()
    if len(sys.argv) > 2 or sys.argv[-1].startswith('-'):
        print '\nUsage: {} [<tests_filepath>]\n'.format(sys.argv[0])
    else:
        tests_filepath = default_tests_filepath
        if len(sys.argv) == 2:
            tests_filepath = sys.argv[1]
        num_errors = run_tests(tests_filepath)
        print 'Elapsed time: {:.1f} seconds\n'.format(time.time() - start)
        exit_code = -1 if num_errors else 0
        exit(exit_code)     # non-zero exit code fails build

