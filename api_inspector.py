import json
import sys



def filter_by_date(api_data, date_wanted):
	elections_on_date = []
	elections = api_data['objects']
	for election in elections:
		end_date = election['end_date']
		if end_date.startswith(date_wanted):
			elections_on_date.append(election)
	return elections_on_date


def print_elections_on_date(date_wanted):
	""" Print election metadata for date wanted.

		Args:
			date_wanted: string
	"""
	json_file = open('elections.json')
	api_data = json.load(json_file)
	elections_on_date = filter_by_date(api_data, date_wanted)
	for election in elections_on_date:
		print json.dumps(election, indent=3)
		print "\n\n\n"
	print "Found ", len(elections_on_date), " elections in/on ", date_wanted 



if __name__ == "__main__":
	if len(sys.argv) == 2:
		print_elections_on_date(sys.argv[1])