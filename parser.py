from wigab.parser import get_offices
from wigab.parser import parse_sheet
from wigab.parser import process_all
import xlrd
import unicodecsv as csv

def process_local(filename):
    results = []
    xlsfile = xlsfile = xlrd.open_workbook(filename)
    offices = get_offices(xlsfile)
    for office in offices:
        index = [x for x in offices].index(office)
        sheet = xlsfile.sheets()[index+1]
        print "parsing %s" % office
        results.append(parse_sheet(sheet, office))

    return results

def _2014_general_ward_results():
  results = process_local("local_data_cache/11.4.2014 Election Results - all offices w x w report.xlsx")
  #results = process_all("http://www.gab.wi.gov/sites/default/files/11.4.2014%20Election%20Results%20-%20all%20offices%20w%20x%20w%20report.xlsx", "11.4.2014%20Election%20Results%20-%20all%20offices%20w%20x%20w%20report.xlsx")
  myfile = open('2014/20141104__wi__general.csv', 'wb')
  wr = csv.writer(myfile)
  for result in results:
    wr.writerows(result)

_2014_general_ward_results()
