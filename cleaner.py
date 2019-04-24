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


office_names = [
    # federal
    'President', 'Senate', 'House',

    # statewide
    'Governor', 'Lieutenant Governor', 'Attorney General',
    'Secretary of State', 'State Treasurer',
    'State Superintendent of Public Instruction',

    # state representatives
    'State Senate', 'State Assembly',

    # judicial, D.A.
    'Supreme Court',
    'Court of Appeals',         # followed by ', District __'
    'Circuit Court',            # __ County Circuit Court[, Branch __]
    'District Attorney',        # __ County District Attorney
]


short_office_names = [
    'President', 'Senate', 'House',
    'Governor', 'Lt Gov', 'Atty General',
    'Sec of St', 'St Treasurer', 'Supt Public Instr',
    'St Senate', 'St Assembly',
    'Supreme Ct', 'Ct Appeals', 'Circuit Ct', 'Dist Atty'
]


offices_requiring_district = [
    'House', 'State Senate', 'State Assembly', 'Court of Appeals']



def normalize_office(office):
    """Generalize office name (remove county, branch)"""
    _, sep, tail = office.rpartition(' County ')
    office = tail       # remove county
    head, sep, tail = office.partition(', Branch ')
    office = head       # remove branch
    return office.strip()


def clean_county(item):
    item = clean_string(item)
    item = item.replace(" County", '')
    item = item.replace("Lacrosse", "La Crosse")
    item = item.replace(" Du ", " du ")     # Fond du Lac
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
    item = item.replace("Special Primary ", "", 1)
    item = office_recode.get(item, item)
    item = item.replace(" Of ", " of ")
    return item

def clean_district(item):
    item = item.strip()
    return int(item) if item.isdigit() else ''

def clean_total(item):
    return to_int(item)

def clean_party(item):
    return party_recode.get(item, item)

def clean_votes(item):
    return to_int(item)

def clean_candidate(item):
    item = item.strip()
    # handle candidate pairs
    item = item.replace("\n"," & ")
    item = item.replace("/"," &")
    item = titlecase_parts(item, ' & ')
    item = titlecase_parts(item, ' Jr.')
    item = titlecase_parts(item, ' Mc')
    head, sep, tail = item.partition(' (')
    if sep:     # probably "(write-in)"
        head = head.title() if head.isupper() else head
        item = head + sep + tail.title()
    item = item.replace("  "," ")
    item = item.replace("Iii","III")
    item = item.replace("Ii","II")
    item = item.replace("(Write In)", "(Write-In)")
    return item

def titlecase_parts(text, separator):
    """Split text by separator, titlecase any uppercase parts, rejoin"""
    parts = text.split(separator)
    parts = [part.title() if part.isupper() else part
                for part in parts]
    return separator.join(parts)


def check_district_appropriate_for_office(row):
    office, district = row[2:4]
    msg = ''
    if office in offices_requiring_district:
        if district == '':
            msg = 'District value missing when required by office'
    else:
        if district != '':
            msg = 'District value present when not appropriate for office'
    if msg:
        raise ValueError(msg + ':\n' + str(row) + '\n')


def clean_row(row):
    for i, clean_func in enumerate([
            clean_county, clean_ward, clean_office, clean_district,
            clean_total, clean_party, clean_candidate, clean_votes]):
        row[i] = clean_func(row[i])
    check_district_appropriate_for_office(row)
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
    """Corrections for specific elections,
        done before clean_row()"""
    id = election['id']
    if id in (411, 413, 1662, 1830):
        row[1] = row[1].replace("!","1")                # ward
    if id == 411:
        row[6] = row[6].replace("   "," ")              # candidate
    if id == 425:
        row[6] = row[6].replace("RICk","RICK")  # candidate, titlecased later
    return row
