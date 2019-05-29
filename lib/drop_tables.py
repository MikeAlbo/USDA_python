import sqlite3


def drop_table(db_cur, table):
    try:
        db_cur.execute('DROP TABLE IF EXISTS %s' % table)
        print(table, "removed")
    except sqlite3.Error:
        print("Error dropping table: %s" % table)


def drop_all_tables(db_cur):
    try:
        db_cur.executescript('''
            DROP TABLE IF EXISTS Products;
            DROP TABLE IF EXISTS Manufactures;
            DROP TABLE IF EXISTS Ingredients;
            DROP TABLE IF EXISTS Nutrients;
            DROP TABLE IF EXISTS Units;
            DROP TABLE IF EXISTS Derivation;
            DROP TABLE IF EXISTS NutrientCodes;
            DROP TABLE IF EXISTS Serving_sizes;
            DROP TABLE IF EXISTS Household_uom;
            DROP TABLE IF EXISTS Long_names;
            ''')
        print("all tables removed")
    except sqlite3.Error:
        print("Error dropping tables")
        print(sqlite3.Error.with_traceback())

