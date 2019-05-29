import csv
import sqlite3


print('''Welcome to the USDA data set parser\n
Products.csv should be located in the raw_data folder
''')

if input("Ready to go? (y/n)").lower() != "y":
    print("python... out!")
    quit()


db_connection = sqlite3.connect("../db/USDA2.sqlite")
cur = db_connection.cursor()

# temp!! use while testing code
cur.execute('DROP TABLE IF EXISTS Products')
cur.execute('DROP TABLE IF EXISTS Manufactures')
cur.execute('DROP TABLE IF EXISTS Ingredients')

cur.executescript('''
    CREATE TABLE IF NOT EXISTS Products (
    product_id INTEGER PRIMARY KEY, ndb_number INTEGER UNIQUE, long_name TEXT UNIQUE,
    gtin_upc INTEGER UNIQUE, manufacture_id INTEGER, ingredients_id INTEGER
    );
    
    CREATE TABLE IF NOT EXISTS Manufactures (
    manufacture_id INTEGER PRIMARY KEY, manufacture_name TEXT UNIQUE
    );
    
    CREATE TABLE IF NOT EXISTS Ingredients (
    ingredient_id INTEGER PRIMARY KEY, ingredients TEXT UNIQUE
    );
''')


file_paths = ['../raw_data/Products.csv']
count = 0
first_line = True


def read_file(file_path):
    try:
        return open(file_path)
    except FileNotFoundError:
        print("%s is an invalid file path" % file_path)
        quit()


with read_file(file_paths[0]) as csvFile:
    csv_reader = csv.reader(csvFile, delimiter=',')
    for row in csv_reader:

        if first_line is True:
            first_line = False
            continue

        # NDB_number = row[0]
        # long_name = row[1]
        # gtin_upc = row[3]
        # manufacture = row[4]
        # ingredients = row[7]

        cur.execute('INSERT OR IGNORE INTO Manufactures (manufacture_name) VALUES (?)', (row[4],))
        cur.execute('SELECT manufacture_id FROM Manufactures WHERE manufacture_name=? LIMIT 1', (row[4],))
        manufacture_id = cur.fetchone()[0]

        cur.execute('INSERT OR IGNORE INTO Ingredients (ingredients) VALUES (?)', (row[7],))
        cur.execute('SELECT ingredient_id FROM Ingredients WHERE ingredients=? LIMIT 1', (row[7],))
        ingredient_id = cur.fetchone()[0]

        cur.execute('''INSERT OR IGNORE INTO Products (ndb_number, long_name, gtin_upc, manufacture_id, ingredients_id)
        VALUES (?, ?, ?, ?, ?)''',
                    (row[0], row[1], row[3], manufacture_id, ingredient_id))

        count += 1

        if count % 5 == 0:
            db_connection.commit()
            count = 0


db_connection.commit()
print("Products Loaded")
first_line = True

# with read_file(file_paths[1]) as csvFile:
#     csv_reader = csv.reader(csvFile, delimiter=',')
#     for row in csv_reader:
#
#         if first_line is True:
#             first_line = False
#             continue

cur.close()
