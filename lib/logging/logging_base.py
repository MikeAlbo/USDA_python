from lib.helpers.helpers import db_name_suffix, path_suffix
from lib.helpers.os_provider import ensure_db, ensure_dir
from lib.sql.db_provider import DbProvider
import time as t


class LogBase:
    """
        5. method that is called that shows how many errors, prompts option to view errors
        6. argument that enables/ disables error logging
        7. argument to delete error logs upon startup
        8. prompt for user to delete current/ last errors
    """
    log_db = None  # initially there is not database connection
    log_cache = list()

    def __init__(self, db_path, db_name):
        """ creates a db_path and db_name var"""
        self.db_path = db_path
        self.db_name = db_name

    def add_message(self, message):
        """called from the method that is generating the log entry, captures timestamp, adds to log"""
        message_time = t.process_time()
        self.log_cache.append((message, message_time))
        if len(self.log_cache) % 20 == 0:
            self._commit_log_db()

    def _create_log_db(self):
        """private: creates connects to the db, if it doesnt exist"""
        self.db_path = path_suffix(self.db_path)
        self.db_name = db_name_suffix(self.db_name)
        full_path = self.db_path + self.db_name
        ensure_dir(self.db_path)
        ensure_db(self.db_name)
        self.log_db = DbProvider(full_path)

    def _commit_log_db(self):
        """private:  ensures db exist, commits the log cache to the db"""
        if self.log_db is None:
            self._create_log_db()
        self.log_db.commit()

    @staticmethod
    def _list_out_log_entries(log_source):
        """private: called by a method to print the entries provided"""
        # convert to use timestamp, should only be 2 positions in entry
        for ls in log_source:
            temp = ""
            for i in ls:
                temp += "%s - " % i
            print(temp)

