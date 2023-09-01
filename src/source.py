import csv
from src.database import DBManager
import src.parser as parser
import os
from io import StringIO

BATCH_SIZE = 1000

def get_manager():
    return DBManager(
        host = os.environ.get("DB_HOST"),
        user = os.environ.get("DB_USER"),
        password = os.environ.get("DB_PASSWORD"),
        database = os.environ.get("DB_DATABASE"),
    )

def check_table(table:str):
    try:
        parse_func = getattr(parser, "parse_{0}".format(table))
        return True
    except:
        pass
    return False

def truncate_table(table:str):
    db_manager = get_manager()
    truncate_func = getattr(db_manager, "truncate_{0}".format(table))
    logs = truncate_func()
    return logs

def insert_csv_to_db(table:str, file:bytes):
    db_manager = get_manager()
    file_reader = csv.reader(file)
    insert = getattr(db_manager,"insert_{0}".format(table))
    parse_func = getattr(parser, "parse_{0}".format(table))

    records_to_insert = []
    logs = []

    while True:
        try:
            record = tuple(
                parse_func(
                    next(file_reader)
                )
            )
            records_to_insert.append(record)

            if len(records_to_insert) == BATCH_SIZE:
                log = insert(records_to_insert)
                logs.append(log)
                records_to_insert = []

        except StopIteration:
            if records_to_insert:
                log = insert(records_to_insert)
                logs.append(log)
            break

    return logs

def query_data(query, year):
    db_manager = get_manager()
    query_function = getattr(db_manager,"query_{0}".format(query))
    header, results = query_function(year)
    out = StringIO()
    csv_out=csv.writer(out)
    csv_out.writerow([struct[0] for struct in header])
    csv_out.writerows(results)
    return out.getvalue()