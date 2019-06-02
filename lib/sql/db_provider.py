
# create errors log, write logs to disk

import sqlite3
from helpers.os_provider import ensure_db, ensure_dir
from helpers.helpers import db_name_suffix, path_suffix
from sql.db_tables import get_drop_table_list, get_create_table_list


class DbProvider:

    connection = None
    cursor = None
    _db_log = list()

    def __init__(self, full_path):

        """set the full db_path, make the db connection and provide the cursor"""

        self._db_path = full_path
        self._make_connection()
        self._set_cursor()

    def get_db_path(self):
        """returns the relative path to the database from the current working directory"""
        return self._db_path

    def _make_connection(self):
        """makes a connection to the sqlite database"""
        try:
            self.connection = sqlite3.connect(self.get_db_path())
            self._append_log("connection made")
        except sqlite3.Error as e:  # todo: convert to static method
            self._append_log(('ERROR: make_connection', e.args[0]))

    def _set_cursor(self):
        """set the database cursor"""
        self.cursor = self.connection.cursor()

    def close_connection(self):
        """close the database connection, auto commits any remaining data"""
        try:
            self.commit()
            self.cursor.close()
            self._append_log(("Connection closed",))
        except self._sql_error() as e:
            self._append_log(("close connection error: ", e.args[0]))

    def commit(self):
        """commits to the database"""
        self.connection.commit()

    def _append_log(self, message):
        """append dbProvider messages to the log"""
        self._db_log.append(message)

    def view_log(self):
        """view the current entries in the db_log"""
        for m in self._db_log:
            print(m)

    def create_tables(self, tables):
        """creates tables from an array of strings containing SQL code"""
        try:
            for table in tables:
                self.cursor.execute(table)
            self._append_log("tables created")
        except self._sql_error() as e:
            self._append_log(e)
            self.view_log()

    def drop_tables(self, tables):
        """drops ALL tables provided by an array of strings containing SQL code"""
        try:
            for table in tables:
                self.cursor.execute(table)
            self._append_log("all tables dropped")
        except sqlite3.Error as e:
            self._append_log(e.args[0])
            self.view_log()

    def execute_sql(self, sql, params):
        """take in the appropriate SQL code and params as a tuple for a single execution"""
        try:
            self.cursor.execute(sql, params)
            self._append_log(("SQL Execute successful:", sql, params))
        except self._sql_error() as e:
            self._append_log(e)
            self.view_log()

    def fetch_one(self):
        """preforms the cursor.fetch_one function and returns an error upon TypeError"""
        try:
            f = self.cursor.fetchone()[0]
            self._append_log(("SQL fetch_one successful:",))
            return f
        except TypeError:
            self._append_log(("SQL fetch_one Error:",))
            self.view_log()

    def fetch_all(self):
        """preforms the cursor.fetch_many function and returns an error upon TypeError"""
        try:
            f = self.cursor.fetchall()
            self._append_log(("SQL fetch_many successful:",))
            return f
        except TypeError:
            self._append_log(("SQL fetch_many Error:",))
            self.view_log()

    @staticmethod
    def _sql_error():
        return sqlite3.Error.args[0]


#  test!! ===================

new_db = DbProvider("../../demo_db", "demo1")
print(new_db.get_db_path())
new_db.drop_tables(get_drop_table_list())
new_db.create_tables(get_create_table_list())
new_db.close_connection()
new_db.view_log()
