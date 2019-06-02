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

            ndb = row[0]
            serving_size = row[1]
            serving_size_uom = row[2]
            household_serving_size = row[3]
            household_serving_size_uom = row[4]

            # serving_size_uom

            usda_db.db.execute_sql('INSERT OR IGNORE INTO Units (unit) Values (?)', (serving_size_uom,))
            serving_size_uom_id = usda_db.sel_rtn_id('''SELECT uom_id FROM Units WHERE unit=? LIMIT 1''', (serving_size_uom,))

            # household_serving_size_uom
            usda_db.db.execute_sql('INSERT OR IGNORE INTO Household_uom (unit) Values (?)', (household_serving_size_uom,))
            household_serving_size_uom_id = usda_db.sel_rtn_id('''SELECT household_uom_id FROM 
            Household_uom WHERE unit=? LIMIT 1''', (household_serving_size_uom,))

            # serving_size
            try:
                product_id = usda_db.sel_rtn_id('''SELECT product_id 
                FROM Products WHERE ndb_number=? LIMIT 1''', (ndb,))
            except TypeError:
                rows_not_added += 1
                print("row not added")
                continue

            usda_db.db.execute_sql('''INSERT OR IGNORE INTO Serving_sizes
            (product_id, serving_size, serving_size_uom, household_serving_size, 
            household_serving_size_uom) VALUES (?, ?, ?, ?, ?)''', (product_id, serving_size, serving_size_uom_id,
                                                                    household_serving_size,
                                                                    household_serving_size_uom_id))

            count += 1
            print("added: ", count)
            if count % 20 == 0:
                usda_db.db.commit()

    usda_db.db.commit()
    print("\n______________________")
    print("DONE LOADING SERVING SIZES")
    print(count, "Rows Parsed")
    print("errors: ", errors)
    print("rows not added: ", rows_not_added)