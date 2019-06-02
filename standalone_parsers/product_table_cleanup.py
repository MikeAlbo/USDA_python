
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


count = 0
product_rows_deleted = 0


def move_row(move_product_id):
    try:
        cur.execute('SELECT * FROM Products WHERE product_id=? LIMIT 1', (move_product_id,))
        moved_product = cur.fetchone()
        cur.execute('''INSERT OR IGNORE INTO Deleted_Products 
                    (product_id, ndb_number, long_name, gtin_upc, manufacture_id, ingredients_id)
                    VALUES (?, ?, ?, ?, ?)''', (moved_product[0], moved_product[1], moved_product[2], moved_product[3], moved_product[4], moved_product[5]))
        cur.execute('''DELETE FROM Products WHERE product_id=?''', (move_product_id,))

        if product_rows_deleted % 10 == 0:
            db_connection.commit()

    except:
        print("row not moved")


cur.execute('SELECT product_id FROM Products')
product_id_column = cur.fetchall()

for product_id in product_id_column:

    p_id = product_id[0]

    try:
        cur.execute('SELECT * FROM Nutrients WHERE product_id=? LIMIT 1', (p_id,))
        _ = cur.fetchone()
        cur.execute('SELECT * FROM Serving_sizes WHERE product_id=? LIMIT 1', (p_id,))
        _ = cur.fetchone()
        print(p_id, "- ok")
    except TypeError:
        product_rows_deleted += 1
        print("\n", p_id, "- removed\n ")
        move_row(p_id)


print("in", count)
print("not in", product_rows_deleted)
db_connection.commit()

db_connection.close()
