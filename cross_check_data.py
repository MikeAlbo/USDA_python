import sqlite3


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

cur.execute('SELECT product_id FROM Products')
product_ids = cur.fetchall()

cur.execute('SELECT product_id FROM Nutrients')
nutrition_ids = cur.fetchall()

cur.execute('SELECT product_id FROM Serving_sizes')
serving_sizes_ids = cur.fetchall()

bad_count = 0
count_down = len(product_ids)
product_rows_deleted = 0
rows_not_deleted = 0


def move_row(move_product_id):
    try:
        cur.execute('SELECT * FROM Products WHERE product_id=? LIMIT 1', (move_product_id,))
        moved_product = cur.fetchone()
        print(moved_product)
        cur.execute('''INSERT OR IGNORE INTO Deleted_Products 
                    (product_id, ndb_number, long_name, gtin_upc, manufacture_id, ingredients_id)
                    VALUES (?, ?, ?, ?, ?, ?)''', (moved_product[0], moved_product[1], moved_product[2], moved_product[3], moved_product[4], moved_product[5]))
        cur.execute('''DELETE FROM Products WHERE product_id=?''', (move_product_id,))

        if product_rows_deleted % 10 == 0:
            db_connection.commit()

        return 0

    except:
        print("row not moved")
        return 1


print("retrieving data...")


for p_id in product_ids:
    count_down -= 1
    if p_id in nutrition_ids and p_id in serving_sizes_ids:
        print(count_down)
        continue
    else:
        bad_count += 1
        product_rows_deleted += 1
        rows_not_deleted += move_row(p_id[0])

db_connection.commit()
print("\n\n----- done -----\n\n")
print("bad: ", bad_count)
print("rows deleted:", product_rows_deleted)
print("rows needed deleted but not: ", rows_not_deleted)


db_connection.close()
