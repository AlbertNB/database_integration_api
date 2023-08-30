import csv
from src.database import DBManager
import src.parser as parser
import os

BATCH_SIZE = 1000

def get_manager():
    return DBManager(
        host = os.environ.get("HOST"),
        user = os.environ.get("USER"),
        password = os.environ.get("PASSWORD"),
        database = os.environ.get("DATABASE"),
    )

def check_table(table:str):
    try:
        parse_func = getattr(parser, "parse_{0}".format(table))
        return True
    except:
        pass
    return False

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
