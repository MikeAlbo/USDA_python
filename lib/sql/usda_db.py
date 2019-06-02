from lib.sql.db_tables import get_drop_table_list, get_create_table_list
from lib.sql.db_provider import DbProvider
from lib.helpers.os_provider import ensure_db, ensure_dir
import lib.helpers.helpers as helpers


class UsdaDb:

    db = None

    def init_usda_db(self, path, db_name):
        path = helpers.path_suffix(path)
        db_name = helpers.db_name_suffix(db_name)
        ensure_dir(path)
        full_path = path + db_name
        ensure_db(full_path)
        self.db = DbProvider(full_path)
        self.drop_all_usda_tables()  # todo: remove
        self.create_usda_tables()
        self.init_parser_complete_table()

    # parser complete methods

    def init_parser_complete_table(self):
        sql = '''INSERT OR IGNORE INTO Parsers_ran 
        (product_parser, nutrition_parser, serving_parser) 
        VALUES (?, ?, ?)'''

        params = (0, 0, 0)

        self.db.execute_sql(sql, params)
        self.db.commit()
        print("parser_complete_table  created!")

    def parser_ran_complete(self, parser):
        sql = '''UPDATE Parsers_ran SET "{}"=? 
        WHERE parser_id =?'''.format(parser)

        params = (1, 1)

        self.db.execute_sql(sql, params)
        self.db.commit()

    def completed_parsers(self):
        try:
            sql = '''Select * FROM Parsers_ran WHERE parser_id=?'''
            params = (1,)
            self.db.execute_sql(sql, params)
            fetched = self.db.fetch_all()[0]
            parsers_ran = dict()
            parsers_ran["p_p"] = True if fetched[1] == 1 else False
            parsers_ran["n_p"] = True if fetched[2] == 1 else False
            parsers_ran["s_p"] = True if fetched[3] == 1 else False
            return parsers_ran

        except TypeError as t:
            print("completed parser error:", t.args[0])

    def create_usda_tables(self):
        self.db.create_tables(get_create_table_list())
        print("USDA tables created")

    def drop_all_usda_tables(self):
        self.db.drop_tables(get_drop_table_list())
        print("USDA tables dropped")

    def drop_single_usda_table(self, table_name):
        try:
            for t in get_drop_table_list():
                if t.endswith(table_name):
                    self.db.drop_tables([t])
                    exit()
                raise "{} is not a proper table name".format(table_name)
        except ValueError as v:
            print(v)

    @staticmethod
    def db_running():
        print("DB is running")


usda_db = UsdaDb()

