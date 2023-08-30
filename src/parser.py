from dateutil import parser

def fill_none(field):
    if field == "":
        field = None
    return field

def parse_employees(record):
    record = [fill_none(field) for field in record]
    # Date Handling
    if record[2]:
        record[2] = parser.parse(record[2])
    else:
        record[2] = None

    return record
 
def parse_jobs(record):
    record = [fill_none(field) for field in record]
    return record

def parse_departments(record):
    record = [fill_none(field) for field in record]
    return record
