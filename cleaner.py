# cleaner.py
# Data cleaning for WI OpenElections parser


party_recode = {
    "Americans Elect": "AME",	
    "Constitution": "CON",
    "Democratic": "DEM",
    "Independent": "IND",
    "Libertarian": "LIB",
    "Republican": "REP",
    "Wisconsin Green": "WGR",
    "Wisconsin Greens": "WGR",
    "Wisconsin Green 2010-09-14": "WIG",
        # WIG appears only in 2010-09-14 primary for Assembly District 77
        # (included here to record all abbreviations)
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
    item = clean_string(item)
    item = item.replace("Lacrosse", "La Crosse")
    return item

def clean_ward(item):
    return clean_string(item)

def clean_office(item):
    item = clean_string(item)
    item = item.replace('Recall ','', 1)    # (first occurrence only, faster)
    item = item.replace(' Judge', '', 1)
    item = item.replace('Circ Ct', 'Circuit Court', 1)
    item = item.replace("Court Branch", "Court, Branch", 1)
    item = item.replace(', Br ', ', Branch ', 1)
    item = item.replace(' And ', '-', 1)
    item = item.replace(' Counties ', ' County ', 1)
    item = item.replace("Lacrosse", "La Crosse", 1)
    office = office_recode.get(item, item)
    return office

def clean_district(item):
    item = item.strip().replace(',','')
    return int(item) if item.isdigit() else None

def clean_total(item):
    return to_int(item)

def clean_party(item):
    return party_recode.get(item, item)

def clean_votes(item):
    return to_int(item)

def clean_candidate(item):
    item = item.replace("\n"," & ")
    item = clean_string(item)
    item = item.replace("/"," &")
    return item

def clean_row(row):
    for i, clean_func in enumerate([
            clean_county, clean_ward, clean_office, clean_district,
            clean_total, clean_party, clean_candidate, clean_votes]):
        row[i] = clean_func(row[i])
    return row

def to_int(item):
    if isinstance(item, basestring):
        item = '0' + item.replace(',','').strip()
    return int(item)

def clean_string(item):
    item = item.strip()
    item = item.replace("\n"," ")
    item = item.replace("  "," ")
    item = item.title()
    return item


def clean_particular(election,row):
    """Corrections for specific elections"""
    id = election['id']
    if id in (411, 413, 1662, 1830):
        row[1] = row[1].replace("!","1")                # ward
    if id == 411:
        row[6] = row[6].replace("   "," ")              # candidate
    return row

