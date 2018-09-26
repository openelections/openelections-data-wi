# -- FILE: features/steps/steps.py

import re
import os.path

from behave import given, when, then, step
from hamcrest import assert_that, has_items, equal_to
import unicodecsv


@when('I visit the election file')
def step_impl(context):
    fileName = re.search('[\-a-z_0-9\.csv]+$',context.scenario.name).group(0)
    year = fileName[:4]
    path = "../%s/%s" % (year, fileName)
    context.path = path

    if (os.path.isfile(path)):
      pass
    else:
      raise AssertionError("%s not found" % path)

@when('I search for {party} party candidate {candidate} running for {office} dist.  in the {ward} in {county}')
def step_impl(context, party, candidate, office, ward, county):
    test(context, party, candidate, office, '', ward, county)

@when('I search for {party} party candidate {candidate} running for {office} dist. {district} in the {ward} in {county}')
def step_impl(context, party, candidate, office, district, ward, county):
    test(context, party, candidate, office, district, ward, county)

def test(context, party, candidate, office, district, ward, county):
    context.passes = False
    field_names = ['party', 'candidate', 'office', 'district', 'ward', 'county']
    if party == '<party>' or party == '':  # No party was specified in the test, don't check party
      field_names.remove('party')
    if district == '<district>' or district == '':  # No district specified, don't check it
      field_names.remove('district')
    expected_values = [locals()[field_name] for field_name in field_names]
    ## Title-case for consistency -- remove this and edit test data instead?
    expected_values = map(unicode.title, expected_values)
    print ("Expecting " + ", ".join(expected_values))

    election_data = unicodecsv.DictReader(open(context.path))
    for row in election_data:
      actual_values = [row[field_name] for field_name in field_names]
      ## Title-case for consistency -- should not be necessary (see above)
      actual_values = map(unicode.title, actual_values)
      if actual_values == expected_values:
        if context.passes:
          raise AssertionError("More than one row found with expected values")
        context.passes = True
        context.votes = row['votes']
        context.total = row['total votes']
    if not context.passes:
      raise AssertionError("No record found with expected values")

@then('I should see {votes} out of {total}')
def step_impl(context,votes,total):
    assert_that(context.votes, equal_to(votes))
    assert_that(context.total, equal_to(total))
