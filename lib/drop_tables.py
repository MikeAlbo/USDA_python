import sqlite3


def drop_table(db_cur, table):
    try:
        db_cur.execute('DROP TABLE IF EXISTS %s' % table)
        print(table, "removed")
    except sqlite3.Error as e:
        print("Error dropping table: %s" % table, e.args[0])


def drop_all_tables(db_cur):
    try:
        db_cur.executescript('''
            DROP TABLE IF EXISTS Products;
            DROP TABLE IF EXISTS Manufactures;
            DROP TABLE IF EXISTS Ingredients;
            DROP TABLE IF EXISTS Nutrients;
            DROP TABLE IF EXISTS Units;
            DROP TABLE IF EXISTS Derivation;
            DROP TABLE IF EXISTS Nutrient_codes;
            DROP TABLE IF EXISTS Serving_sizes;
            DROP TABLE IF EXISTS Household_uom;
            DROP TABLE IF EXISTS Long_names;
            DROP TABLE IF EXISTS Parsers_ran;
            ''')
        print("all tables removed")
    except sqlite3.Error as e:
        print("Error dropping tables")
        print(e.args[0])
