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

@when('I search for candidate {candidate} running for {office} in the {ward}')
def step_impl(context,candidate,office,ward):
    context.passes = False

    election_data = csv.DictReader(open(context.path))
    for row in election_data:
      if (row['candidate'] == candidate and row['ward'] == ward and row['office'] == office):
        context.passes = True
        context.votes = row['votes']
        context.total = row['total votes']
    pass
    if (context.passes):
      pass
    else:
      raise AssertionError("Record not found for {candidate}")

@then('I should see {votes} out of {total}')
def step_impl(context,votes,total):
    assert_that(context.votes, equal_to(votes))
    assert_that(context.total, equal_to(total))
