import csv
import sqlite3

print('''
    USDA Serving Size Table Parser
    Serving_size.csv should be located in the raw_data folder
    ** must run product_table_parser and nutrition_table_parser first **
''')

if input("Ready to go? (y/n)").lower() != "y":
    print("well let me know when you are...")
    quit()

db_connection = sqlite3.connect("../db/USDA2.sqlite")
cur = db_connection.cursor()

# todo: move these to a function that is called by and input argument
cur.execute('DROP TABLE IF EXISTS Serving_sizes')

cur.executescript('''
    CREATE TABLE IF NOT EXISTS Serving_sizes (
        serving_size_id INTEGER PRIMARY KEY, product_id INTEGER, 
        serving_size INTEGER, serving_size_uom INTEGER,
        household_serving_size INTEGER, household_serving_size_uom INTEGER 
    );
''')

file_paths = ['../raw_data/Serving_size.csv']
first_line = True
count = 0
rows_not_added = 0


def read_file(file_path):
    try:
        return open(file_path)
    except FileNotFoundError:
        print("%s is not a valid file path" % file_path)
        quit()


with read_file(file_paths[0]) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    print("parsing csv to db...")
    for row in csv_reader:
        if first_line is True:
            first_line = False
            continue

        ndb = row[0]
        serving_size = row[1]
        serving_size_uom = row[2]
        household_serving_size = row[3]
        household_serving_size_uom = row[4]

        # serving_size_uom
        cur.execute('INSERT OR IGNORE INTO Units (unit) Values (?)', (serving_size_uom,))
        cur.execute('SELECT uom_id FROM Units WHERE unit=? LIMIT 1', (serving_size_uom,))
        try:
            serving_size_uom_id = cur.fetchone()[0]
        except TypeError:
            rows_not_added += 1
            print("uom failed")
            continue

        # household_serving_size_uom
        cur.execute('INSERT OR IGNORE INTO Units (unit) Values (?)', (household_serving_size_uom,))
        cur.execute('SELECT uom_id FROM Units WHERE unit=? LIMIT 1', (household_serving_size_uom,))
        try:
            household_serving_size_uom_id = cur.fetchone()[0]
        except TypeError:
            rows_not_added += 1
            print("family uom failed")
            continue

        # serving_size
        cur.execute('SELECT product_id FROM Products WHERE ndb_number=? LIMIT 1', (ndb,))
        try:
            product_id = cur.fetchone()[0]
        except TypeError:
            rows_not_added += 1
            print("product_id failed")
            continue

        cur.execute('''
        INSERT OR IGNORE INTO Serving_sizes
        (product_id, serving_size, serving_size_uom, household_serving_size, household_serving_size_uom)
        VALUES (?, ?, ?, ?, ?)
        ''', (product_id, serving_size, serving_size_uom_id, household_serving_size, household_serving_size_uom_id))

        count += 1
        if count % 20 == 0:
            db_connection.commit()

db_connection.commit()
print("Finished serving size table")
print("failed: ", rows_not_added)
print(count)
cur.close()
