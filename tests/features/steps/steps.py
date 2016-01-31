# -- FILE: features/steps/steps.py
from behave import given, when, then, step
from hamcrest import assert_that, has_items, equal_to
import re
import os.path
import csv

@when('I visit the election file')
def step_impl(context):
    fileName = re.search('[a-z_0-9\.csv]+$',context.scenario.name).group(0)
    year = fileName[:4]
    path = "../%s/%s" % (year, fileName)
    context.path = path

    if (os.path.isfile(path)):
      pass
    else:
      raise AssertionError("%s not found" % path)

@when('I search for candidate {candidate} running for {office} in the {ward} in {county}')
def step_impl(context,candidate,office,ward,county):
    context.passes = False

    print ("Expecting %s %s %s %s" % (candidate.title(), office.title(), ward.title(), county.title()))

    election_data = csv.DictReader(open(context.path))
    for row in election_data:
      print ("Found %s %s %s %s %s %s" % (row['candidate'], row['office'], row['ward'], row['county'], row['votes'], row['total votes']))
      if (row['candidate'] == candidate.title() and row['ward'] == ward.title() and row['office'] == office.title()  and row['county'] == county.title()):
        context.passes = True
        context.votes = row['votes']
        context.total = row['total votes']
    pass
    if (context.passes):
      pass
    else:
      raise AssertionError("Record not found for %s" % candidate.title())

@then('I should see {votes} out of {total}')
def step_impl(context,votes,total):
    assert_that(context.votes, equal_to(votes))
    assert_that(context.total, equal_to(total))
