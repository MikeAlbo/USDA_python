import os
import sqlite3
import csv


def help_options():
    print("Help!")
    print("===================")
    print('clean - clears previously stored tables')
    print('clean-parse - clears the tables and runs the parser')
    print('rm-db - deletes the current database')
    quit()


def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


def ensure_db(file_name):
    if not os.path.exists(file_name):
        f = open(file_name, 'w')
        f.close()


def check_files_exist(dir_path):
    try:
        _ = os.path.isfile("%s/Products.csv" % dir_path)
        _ = os.path.isfile("%s/Nutrients.csv" % dir_path)
        _ = os.path.isfile("%s/Serving_size.csv" % dir_path)
        print("files found...")
    except TypeError:
        print("Files Not found in ../raw_data dir")
        quit()


def make_db_connection(dir_path, db_name):
    try:
        ensure_dir(dir_path)
        full_path = dir_path + db_name
        ensure_db(full_path)

        return sqlite3.connect(full_path)
    except sqlite3.Error:
        print("There was an issue creating the DB...")
        quit()


def init_parser_complete_table(cursor, db_connection):
    cursor.execute('''INSERT OR IGNORE INTO Parsers_ran 
    (product_parser, nutrition_parser, serving_parser) 
    VALUES (?, ?, ?)''', (0, 0, 0))
    db_connection.commit()


def parser_ran_complete(cursor, db_connection, parser):
    cursor.execute('''UPDATE Parsers_ran SET 
    "{}"=? 
    WHERE parser_id =?'''.format(parser), (1, 1))
    db_connection.commit()


def completed_parsers(cursor):
    try:
        cursor.execute("Select * FROM Parsers_ran WHERE parser_id=?", (1,))
        fetched = cursor.fetchall()[0]
        parsers_ran = dict()
        parsers_ran["p_p"] = True if fetched[1] == 1 else False
        parsers_ran["n_p"] = True if fetched[2] == 1 else False
        parsers_ran["s_p"] = True if fetched[3] == 1 else False
        return parsers_ran
    except TypeError as t:
        print("completed parser error:", t.args[0])


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
