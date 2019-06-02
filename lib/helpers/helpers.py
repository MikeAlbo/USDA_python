
import csv
from lib.sql.usda_db import usda_db


def product_parser_check():
    if usda_db.completed_parsers()["p_p"] is False:
        print("product parser needs to run first")
        quit()


def all_parsers_complete():
    for v in usda_db.completed_parsers().values():
        if v is False:
            print("All parsers must be run before you are able to clean the data")
            quit()


def read_file(file_path):
    try:
        return open(file_path)
    except FileNotFoundError:
        print("%s is an invalid file path" % file_path)
        quit()


def read_csv(csv_file):
    try:
        return csv.reader(csv_file, delimiter=",")
    except csv.Error:
        print(csv.Error)
        quit()


def db_name_suffix(name):
    """ensure that the db name provided ends in the .sqlite format"""
    return name if str(name).endswith(".sqlite") else name + ".sqlite"


def path_suffix(path):
    """ensure that the path provided ends with an '/' to create a proper dir"""
    return path if str(path).endswith("/") else path + "/"
