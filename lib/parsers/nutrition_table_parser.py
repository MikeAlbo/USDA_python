def main(file_path, cursor, db_connection):
    import sqlite3
    from helpers.helpers import read_file, read_csv

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

            nbd = row[0]
            nutrient_code = row[1]
            nutrient_name = row[2]
            derivation = row[3]
            output_val = row[4]
            uom = row[5]

            # units
            try:
                cursor.execute('INSERT OR IGNORE INTO Units (unit) VALUES (?)', (uom,))
                cursor.execute('SELECT uom_id FROM Units WHERE unit=? LIMIT 1', (uom,))
                uom_id = cursor.fetchone()[0]
            except sqlite3.Error as e:
                print("Insert error into units", e.args[0])
                errors += 1

            # derivation
            try:
                cursor.execute('INSERT OR IGNORE INTO Derivation (derivation_code) VALUES (?)', (derivation,))
                cursor.execute('SELECT derivation_id FROM Derivation WHERE derivation_code=? LIMIT 1', (derivation,))
                derivation_id = cursor.fetchone()[0]
            except sqlite3.Error as e:
                print("Insert error into Derivation", e.args[0])
                errors += 1

            # nutrientCode
            try:
                cursor.execute('INSERT OR IGNORE INTO Nutrient_codes (nutrient_code, nutrient_name) VALUES (?, ?)',
                               (nutrient_code, nutrient_name))
            except sqlite3.Error as e:
                print("Insert error into Nutrient_codes", e.args[0])
                errors += 1

            # product_id
            cursor.execute('SELECT product_id FROM Products WHERE ndb_number=? LIMIT 1', (nbd,))
            try:
                product_id = cursor.fetchone()[0]
            except TypeError:
                rows_not_added += 1
                continue

            try:
                cursor.execute('''INSERT OR IGNORE INTO Nutrients 
                                                (product_id, nutrient_code, uom_id, derivation_id, output_value)
                                                VALUES (?, ?, ?, ?, ?)''',
                            (product_id, nutrient_code, uom_id, derivation_id, output_val))
            except sqlite3.Error as e:
                print("Insert error into Nutrients", e.args[0])
                errors += 1

            count += 1
            if count % 20 == 0:
                db_connection.commit()
                print(count)

        db_connection.commit()
        print("\n______________________")
        print("DONE LOADING NUTRIENTS")
        print(count, "Rows Parsed")
        print("errors: ", errors)
        print("rows not added: ", rows_not_added)

