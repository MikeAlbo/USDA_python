from lib.helpers.helpers import db_name_suffix, path_suffix
from lib.helpers.os_provider import ensure_db, ensure_dir
from lib.sql.db_provider import DbProvider
import time as t


class ErrorHandle:
    """
        5. method that is called that shows how many errors, prompts option to view errors
        6. argument that enables/ disables error logging
        7. argument to delete error logs upon startup
        8. prompt for user to delete current/ last errors
    """
    error_db = None  # initially there is not database connection
    error_log_cache = list()

    def __init__(self, db_path, db_name, handle_error):
        """ creates a db_path and db_name var, and sets whether or not the user wants to log errors """
        self.db_path = db_path
        self.db_name = db_name
        self.handle_errors = handle_error

    def add_error(self, error):
        """called from the method that is generating the error, captures timestamp, adds to log"""
        error_time = t.process_time()
        self.error_log_cache.append((error, error_time))
        if len(self.error_log_cache) % 20 == 0:
            self._commit_error_db()

    def _create_error_db(self):
        """private: creates connects to the db, if it doesnt exist"""
        self.db_path = path_suffix(self.db_path)
        self.db_name = db_name_suffix(self.db_name)
        full_path = self.db_path + self.db_name
        ensure_dir(self.db_path)
        ensure_db(self.db_name)
        self.error_db = DbProvider(full_path)

    def _commit_error_db(self):
        """private:  ensures db exist, commits the error cache to the db"""
        if self.error_db is None:
            self._create_error_db()
        self.error_db.commit()

    @staticmethod
    def _list_out_errors(error_source):
        """private: called by a method to print the errors provided"""
        # convert to use timestamp, should only be 2 positions in each error
        for error in error_source:
            temp = ""
            for e in error:
                temp += "%s - " % e
            print(temp)

