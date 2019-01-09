"""
run_spot_tests.py
Check for example records in CSV results files output by parser
David "Davi" Post, 2019-01
for OpenElections project in WI
"""

import sys
import time

import unicodecsv as csv


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

# Fields in testing order
fields = ['office', 'district', 'county', 'ward', 'candidate', 'party',
            'votes', 'total votes']
fields = [unicode(field) for field in fields]


def test_result_file(filename, tests):
    """Check that records in tests appear exactly once in named file.
        tests is a list of tests,
        each test is a dict containing test data as field:value.
    """
    print 'Testing', filename
    year = filename[:4]
    assert year.isdigit()
    filepath = year + '/' + filename
    
    with open(filepath) as results_file:
        reader = csv.DictReader(results_file)
        test_counts = [0] * len(tests)   # number of times test data found
        for record in reader:
            for i, test in enumerate(tests):
                for field in fields:
                    if record[field] != test[field]:
                        if field == 'party' and test[field] == '':
                            continue    # ignore blank party in test
                        break
                else:   # no break, test data found
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
            print ', '.join([test[field] for field in fields])
            num_errors += 1
    return num_errors


def run_tests(tests_filepath):
    """Read tests for each results file, check for specified records"""
    tests_file = open(tests_filepath)
    tests_reader = csv.DictReader(tests_file)
    num_files = 0
    num_errors = 0
    num_tests = 0
    done = False
    row = tests_reader.next()
    while not done:
        filename = row['filename']
        tests = []
        for row in tests_reader:
            if row['filename']:     # next file to test
                break
            row['total votes'] = row['total']
            del row['total']
            for field in ('office', 'county', 'ward', 'candidate'):
                row[field] = row[field].title()
            tests.append(row)
            
        else:   # no break, end of file
            done = True
        
        num_errors += test_result_file(filename, tests)
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

