# Tabulate offices processed, for WI OpenElections parser

import csv

import cleaner


class OfficeTable(object):
    """Record offices parsed for each election, write to table"""
    FILENAME = 'office_table'

    def __init__(self):
        filename = OfficeTable.FILENAME + '.csv'
        office_table_file = open(filename, 'wt')
        self.writer = csv.writer(office_table_file)
        self.write_header()
        self.offices_per_election = set()
        self.offices_found = set()


    def new_election(self):
        self.offices_per_election.clear()


    def add_office(self, office):
        cleaned_office = cleaner.clean_office(office)
        norm_office = cleaner.normalize_office(cleaned_office)
        if norm_office not in cleaner.office_names:
            raise Exception('Unrecognized office name: ' + cleaned_office)
        self.offices_per_election.add(norm_office)


    def write_header(self):
        note = '*** Append these records to {}.xlsx ***'.format(
            OfficeTable.FILENAME)
        self.writer.writerow([note])
        self.headers = [
            'id', 'date', 'special', 'primary', 'recall', 'no_data']
        self.headers += cleaner.short_office_names
        self.writer.writerow(self.headers)


    def tabulate_offices(self, election):
        self.offices_found.update(self.offices_per_election)
        info = [election['id'], election['end_date']]
        info.append('S' if election['special'] else '')
        info.append('P' if election['race_type'].startswith('primary') else '')
        info.append('R' if election['race_type'].endswith('-recall') else '')
        info.append('' if self.offices_per_election else 'nd')  # no data
        for name in cleaner.office_names:
            info.append(
                'X' if name.title() in self.offices_per_election else '')
        self.writer.writerow(info)


    def print_summary(self):
        num_offices_found = len(self.offices_found)
        print('\n{} offices processed:'.format(num_offices_found))
        print('\n'.join(sorted(self.offices_found)))
