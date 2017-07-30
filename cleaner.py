
import re


party_recode = {
    "Constitution": "CON",
    "Democratic": "DEM",
    "Independent": "IND",
    "Libertarian": "LIB",
    "Republican": "REP",
    "Wisconsin Green": "WGR",
    "Wisconsin Greens": "WGR",
    "Wisconsin Green 2010-09-14": "WIG",  # only in 2010-09-14 primary Assembly District 77
    "Non-Partisan": "NP",
    "not applicable?": "NA"
}

"""Recode office names to conform to
    https://github.com/openelections/specs/wiki/Office-Names
    -- except for State Senate and State Assembly.
    Keys in this map should be in titlecase.
"""
office_recode = {
    'President Of The United States': 'President',
    'Us Senator': 'Senate',
    'Us Senate': 'Senate',
    'United States Senator': 'Senate',
    'Us Congress': 'House',
    'Representative In Congress': 'House',
    'Congressional': 'House',
    'Governor/Lieutenant Governor': 'Governor',
    'Justice Of The Supreme Court': 'Supreme Court',
    'State Senator': 'State Senate',
    'Assembly': 'State Assembly',
    'Representative To The Assembly': 'State Assembly',
}


### To Do: Check that office is one of these?
office_names = [
    # federal
    'President', 'Senate', 'House',
#     'President', 'US Senate', 'US House',
    
    # statewide
    'Governor', 'Lieutenant Governor', 'Attorney General',
    'Secretary of State', 'State Treasurer',
    'State Superintendent of Public Instruction',
    
    # judges
    'Supreme Court', 'Court of Appeals[, District __]',
    '__ County Circuit Court[, Branch __]',
    
    # state representatives
    'State Senate', 'State Assembly',
    
    # county offices
    '__ County District Attorney',
]


def clean_county(item):
    return clean_string(item)

def clean_ward(item):
    return clean_string(item)

def clean_office(item):
    item = item.title()
    item = item.replace(' Judge', '', 1)    # remove first occurrence
    office = office_recode.get(item)
    if office is None:
        office = clean_string(item)
    return office

def clean_district(item):
    item = item.strip()
    if re.match(r"[0-9,]+", item):
        return to_int(item)
    else:
        return None

def clean_total(item):
    return to_int(item)

def clean_party(item):
    code = party_recode.get(item)
    return code if code else item

def clean_votes(item):
    return to_int(item)

def clean_candidate(item):
    item = item.replace("\n"," & ")
    item = clean_string(item)
    item = item.replace("/"," &")
    return item

def clean_row(row):
    row[0] = clean_county(row[0])
    row[1] = clean_ward(row[1])
    row[2] = clean_office(row[2])
    row[3] = clean_district(row[3])
    row[4] = clean_total(row[4])
    row[5] = clean_party(row[5])
    row[6] = clean_candidate(row[6])
    row[7] = clean_votes(row[7])
    return row

def to_int(item):
    if isinstance(item, basestring):
        item = item.replace(',','').strip()
        if item.isdigit():
            item = int(item)
        elif item == '':
            item = 0
    else:   # assume int or float
        item = int(item)
    return item

def clean_string(item):
    item = item.strip()
    item = item.replace("\n"," ")
    item = item.title()
    return item


# Here is where things get messy.
def clean_particular(election,row):
    id = election['id']
    if id in (411, 413, 1662):
        row[1] = row[1].replace("!","1")
    if id == 424:
        row[2] = row[2].replace(" - 2011-2017","")
    elif id == 1662:
        row[2] = row[2].replace("RECALL ","")
    return row

