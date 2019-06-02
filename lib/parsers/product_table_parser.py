
def main(file_path, cursor, db_connection):

    import sqlite3
    from helpers.helpers import read_file, read_csv

    count = 0
    first_line = True
    errors = 0
    with read_file(file_path) as csv_file:
        csv_reader = read_csv(csv_file)
        for row in csv_reader:

            if first_line is True:
                first_line = False
                continue

            ndb_number = row[0]
            long_name = row[1]
            gtin_upc = row[3]
            manufacture = row[4]
            ingredients = row[7]

            try:
                cursor.execute('INSERT OR IGNORE INTO Manufactures (manufacture_name) VALUES (?)', (manufacture,))
                cursor.execute('SELECT manufacture_id FROM Manufactures WHERE manufacture_name=? LIMIT 1',
                               (manufacture,))
                manufacture_id = cursor.fetchone()[0]
            except sqlite3.Error as e:
                errors += 1
                print("Error during Manufactures:", e.args[0])

            try:
                cursor.execute('INSERT OR IGNORE INTO Ingredients (ingredients) VALUES (?)', (ingredients,))
                cursor.execute('SELECT ingredient_id FROM Ingredients WHERE ingredients=? LIMIT 1', (ingredients,))
                ingredient_id = cursor.fetchone()[0]
            except sqlite3.Error as e:
                errors += 1
                print("Error during Ingredients:", e.args[0])

            try:
                cursor.execute('INSERT OR IGNORE INTO Long_names (long_name) VALUES (?)', (long_name,))
                cursor.execute('SELECT long_name_id FROM Long_names WHERE long_name=? LIMIT 1', (long_name,))
                long_name_id = cursor.fetchone()[0]
            except sqlite3.Error as e:
                errors += 1
                print("Error during long_names:", e.args[0])

            try:
                cursor.execute('''INSERT INTO Products (ndb_number, long_name, gtin_upc, manufacture_id, ingredients_id)
                                    VALUES (?, ?, ?, ?, ?)''',
                               (ndb_number, long_name_id, gtin_upc, manufacture_id, ingredient_id))
            except sqlite3.Error as e:
                errors += 1
                print("Error during Product Insert", e.args[0])

            count += 1

            if count % 20 == 0:
                db_connection.commit()
                print("ndb number: ", ndb_number, "count: ", count)

    db_connection.commit()
    print("\n______________________")
    print("DONE LOADING PRODUCTS")
    print(count, "Rows Parsed")
    print("errors: ", errors)
    print("there are approx 2400 upc duplicates which show up as errors")
