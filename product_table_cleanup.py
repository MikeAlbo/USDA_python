
import sqlite3

print('''-
Product Table cleanup
This "cleanup" will remove products from the the Products table
that do not have corresponding data in rhw Serving_size or Nutrition tables
** must run the three parsers first or your gonna have a bad time! ** 
''')

if input("Ready to go? (y/n) ").lower() != "y":
    print("bye, bye now...")
    quit()

db_connection = sqlite3.connect("../db/USDA2.sqlite")
cur = db_connection.cursor()

# todo: add as function called by argument
cur.execute('DROP TABLE IF EXISTS Deleted_products')

cur.execute('''
    CREATE TABLE IF NOT EXISTS Deleted_Products (
        product_id INTEGER PRIMARY KEY, ndb_number INTEGER UNIQUE, long_name TEXT UNIQUE,
        gtin_upc INTEGER UNIQUE, manufacture_id INTEGER, ingredients_id INTEGER
    )
''')


moved_count = 0

cur.execute('SELECT * FROM Products')
products_table = cur.fetchall()

print("Product 1:", products_table[0])

count = 0
product_rows_deleted = 0


