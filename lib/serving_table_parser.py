def main(file_path, cursor, db_connection):
    import sqlite3
    from lib.helpers import read_file, read_csv

    count = 0
    first_line = True
    errors = 0
    rows_not_added = 0
    
    with read_file(file_path) as csv_file:
        csv_reader = read_csv(csv_file)
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
            try:
                cursor.execute('INSERT OR IGNORE INTO Units (unit) Values (?)', (serving_size_uom,))
                cursor.execute('SELECT uom_id FROM Units WHERE unit=? LIMIT 1', (serving_size_uom,))
                serving_size_uom_id = cursor.fetchone()[0]
            except sqlite3.Error as e:
                errors += 1
                print("Insert Error Units", e.args[0])
                continue

            # household_serving_size_uom
            try:
                cursor.execute('INSERT OR IGNORE INTO Household_uom (unit) Values (?)', (household_serving_size_uom,))
                cursor.execute('''SELECT household_uom_id FROM 
                Household_uom WHERE unit=? LIMIT 1''', (household_serving_size_uom,))
                household_serving_size_uom_id = cursor.fetchone()[0]
            except sqlite3.Error as e:
                errors += 1
                print("Insert Error Household_uom", e.args[0])
                continue

            # serving_size

            try:
                cursor.execute('SELECT product_id FROM Products WHERE ndb_number=? LIMIT 1', (ndb,))
                product_id = cursor.fetchone()[0]

            except TypeError:
                rows_not_added += 1
                print("row not added")
                continue
            # except sqlite3.Error as e:
            #     errors += 11
            #     print("Product Retrieval Error: ", e.args[0])
            #     continue
            try:
                cursor.execute('''
                            INSERT OR IGNORE INTO Serving_sizes
                            (product_id, serving_size, serving_size_uom, 
                            household_serving_size, 
                            household_serving_size_uom)
                            VALUES (?, ?, ?, ?, ?)
                            ''', (
                    product_id, serving_size, serving_size_uom_id,
                    household_serving_size, household_serving_size_uom_id))
            except sqlite3.Error as e:
                errors += 1
                print("Insert Error Serving_sizes: ", e.args[0])

            count += 1
            print("added: ", count)
            if count % 20 == 0:
                db_connection.commit()

    db_connection.commit()
    print("\n______________________")
    print("DONE LOADING SERVING SIZES")
    print(count, "Rows Parsed")
    print("errors: ", errors)
    print("rows not added: ", rows_not_added)