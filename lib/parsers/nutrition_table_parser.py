def main(file_path):
    from lib.helpers.helpers import read_file, read_csv
    from lib.sql.usda_db import usda_db

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
            usda_db.db.execute_sql('''INSERT OR IGNORE INTO Units (unit) VALUES (?)''', (uom,))
            uom_id = usda_db.sel_rtn_id('''SELECT uom_id FROM Units WHERE unit=? LIMIT 1''', (uom,))

            # derivation
            usda_db.db.execute_sql('INSERT OR IGNORE INTO Derivation (derivation_code) VALUES (?)', (derivation,) )
            derivation_id = usda_db.sel_rtn_id('''SELECT derivation_id 
            FROM Derivation WHERE derivation_code=? LIMIT 1''', (derivation,))

            # nutrientCode
            usda_db.db.execute_sql('''INSERT OR IGNORE INTO 
            Nutrient_codes (nutrient_code, nutrient_name) 
            VALUES (?, ?)''', (nutrient_code, nutrient_name))

            # product_id
            try:
                product_id = usda_db.sel_rtn_id('''SELECT product_id 
                FROM Products WHERE ndb_number=? LIMIT 1''', (nbd,))
            except TypeError:
                rows_not_added += 1
                print("row not added")
                continue

            usda_db.db.execute_sql('''INSERT OR IGNORE INTO Nutrients 
            (product_id, nutrient_code, uom_id, derivation_id, output_value)
            VALUES (?, ?, ?, ?, ?)''', (product_id, nutrient_code, uom_id, derivation_id, output_val))

            count += 1
            if count % 20 == 0:
                usda_db.db.commit()
                print(count)

        usda_db.db.commit()
        print("\n______________________")
        print("DONE LOADING NUTRIENTS")
        print(count, "Rows Parsed")
        print("errors: ", errors)
        print("rows not added: ", rows_not_added)

