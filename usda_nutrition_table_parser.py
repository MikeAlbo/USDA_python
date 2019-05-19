import csv
import sqlite3

print('''
USDA_Nutrition Table Parser 
Nutrients.csv should be located in the raw data folder
** must run product_table_parser.py first ** 
''')

if input("Ready to go? (y/n) ").lower() != "y":
    print("well this was fun...")
    quit()

db_connection = sqlite3.connect("../db/USDA2.sqlite")
cur = db_connection.cursor()

# todo: move to a argument called function, here for db setup/testing
cur.execute('DROP TABLE IF EXISTS Nutrients')
cur.execute('DROP TABLE IF EXISTS Units')
cur.execute('DROP TABLE IF EXISTS Derivation')
cur.execute('DROP TABLE IF EXISTS NutrientCodes')

cur.executescript('''
    CREATE TABLE IF NOT EXISTS Nutrients (
        product_nutrient_id INTEGER PRIMARY KEY, product_id INTEGER, nutrient_code INTEGER, 
        uom_id INTEGER, derivation_id INTEGER, output_value INTEGER
    );
    
    CREATE TABLE IF NOT EXISTS Units (
        uom_id INTEGER PRIMARY KEY, unit TEXT UNIQUE
    );
    
    CREATE TABLE IF NOT EXISTS Derivation (
        derivation_id INTEGER PRIMARY KEY, derivation_code TEXT UNIQUE
    );
    
    CREATE TABLE IF NOT EXISTS NutrientCodes(
        nutrient_code INTEGER PRIMARY KEY, nutrient_name TEXT UNIQUE
    );
''')


# setup raw data import

file_paths = ['../raw_data/Nutrients.csv']
first_line = True
count = 0
rows_not_added = 0

# read the csv file and soft fail if error


def read_file(file_path):
    try:
        return open(file_path)
    except FileNotFoundError:
        print("%s is an invalid file path" % file_path)
        quit()


with read_file(file_paths[0]) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    for row in csv_reader:
        if first_line is True:
            first_line = False
            continue

        nbd = row[0]
        nutrient_code = row[1]
        nutrient_name = row[2]
        derivation = row[3]
        output_val = row[4]
        uom = row[5]

        # units
        cur.execute('INSERT OR IGNORE INTO Units (unit) VALUES (?)', (uom,))
        cur.execute('SELECT uom_id FROM Units WHERE unit=? LIMIT 1', (uom,))
        uom_id = cur.fetchone()[0]

        # derivation
        cur.execute('INSERT OR IGNORE INTO Derivation (derivation_code) VALUES (?)', (derivation,))
        cur.execute('SELECT derivation_id FROM Derivation WHERE derivation_code=? LIMIT 1', (derivation,))
        derivation_id = cur.fetchone()[0]

        # nutrientCode
        cur.execute('INSERT OR IGNORE INTO NutrientCodes (nutrient_code, nutrient_name) VALUES (?, ?)',
                    (nutrient_code, nutrient_name))
        # nutrient code from var

        # nutrients
        cur.execute('SELECT product_id FROM Products WHERE ndb_number=? LIMIT 1', (nbd,))
        try:
            product_id = cur.fetchone()[0]
        except TypeError:
            rows_not_added += 1
            continue

        cur.execute('''INSERT OR IGNORE INTO Nutrients 
                    (product_id, nutrient_code, uom_id, derivation_id, output_value)
                    VALUES (?, ?, ?, ?, ?)''', (product_id, nutrient_code, uom_id, derivation_id, output_val))

        count += 1
        if count % 20 == 0:
            db_connection.commit()
            print(count)

db_connection.commit()
print("Nutrients Loaded")
print("%i rows not added " % rows_not_added)
cur.close()
