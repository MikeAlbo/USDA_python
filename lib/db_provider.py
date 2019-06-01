
# initialize the db with the db name and path
# create a cursor
# create errors log, write logs to disk


import sqlite3
from os_provider import ensure_db, ensure_dir
from helpers import db_name_suffix, path_suffix
from db_tables import get_drop_table_list, get_create_table_list


class DbProvider:

    connection = None
    cursor = None
    _db_log = list()

    def __init__(self, path, db_name):

        path = path_suffix(path)
        db_name = db_name_suffix(db_name)
        ensure_dir(path)  # ensure that the path exist on the user's directory
        ensure_db(path + db_name)  # ensures that the db_name provided exist/ creates file

        self._db_path = path + db_name
        self.make_connection()
        self.set_cursor()

    def get_db_path(self):
        """returns the relative path to the database from the current working directory"""
        return self._db_path

    def make_connection(self):
        """makes a connection to the sqlite database"""
        try:
            self.connection = sqlite3.connect(self.get_db_path())
            self.append_log("connection made")
        except sqlite3.Error as e:
            self.append_log(('ERROR: make_connection', e.args[0]))

    def set_cursor(self):
        self.cursor = self.connection.cursor()

    def close_connection(self):
        self.cursor.close()

    def commit(self):
        self.connection.commit()

    def append_log(self, message):
        self._db_log.append(message)

    def view_log(self):
        for m in self._db_log:
            print(m)

    def create_tables(self):
        try:
            for table in get_create_table_list():
                self.cursor.execute(table)
            self.append_log("tables created")
        except sqlite3.Error as e:
            self.append_log(e.args[0])
            self.view_log()

    def drop_tables(self):
        try:
            for table in get_drop_table_list():
                self.cursor.execute(table)
            self.append_log("all tables dropped")
        except sqlite3.Error as e:
            self.append_log(e.args[0])
            self.view_log()


#  test!! ===================

new_db = DbProvider("../../demo_db", "demo1")
print(new_db.get_db_path())
new_db.drop_tables()
new_db.create_tables()
new_db.close_connection()
new_db.view_log()
