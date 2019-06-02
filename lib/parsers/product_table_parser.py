
def main(file_path):

    from lib.helpers.helpers import read_file, read_csv
    from lib.sql.usda_db import usda_db

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

            usda_db.db.execute_sql('INSERT OR IGNORE INTO Manufactures (manufacture_name) VALUES (?)', (manufacture,))
            manufacture_id = usda_db.select_return_id('''SELECT manufacture_id 
            FROM Manufactures WHERE manufacture_name=? LIMIT 1''', (manufacture,))

            usda_db.db.execute_sql('''INSERT OR IGNORE INTO Ingredients (ingredients) VALUES (?)''', (ingredients,))
            ingredient_id = usda_db.select_return_id('''SELECT ingredient_id 
            FROM Ingredients WHERE ingredients=? LIMIT 1''', (ingredients,))

            usda_db.db.execute_sql('''INSERT OR IGNORE INTO Long_names (long_name) VALUES (?)''', (long_name,))
            long_name_id = usda_db.select_return_id('''SELECT long_name_id 
            FROM Long_names WHERE long_name=? LIMIT 1''', (long_name,))

            try:
                usda_db.db.execute_sql('''INSERT INTO Products 
                (ndb_number, long_name, gtin_upc, manufacture_id, ingredients_id)
                VALUES (?, ?, ?, ?, ?)''', (ndb_number, long_name_id, gtin_upc, manufacture_id, ingredient_id))
            except:
                errors += 1
                print("error!")

            count += 1

            if count % 20 == 0:
                usda_db.db.commit()
                print("ndb number: ", ndb_number, "count: ", count)

    usda_db.db.commit()
    print("\n______________________")
    print("DONE LOADING PRODUCTS")
    print(count, "Rows Parsed")
    print("errors: ", errors)
    print("there are approx 2400 upc duplicates which show up as errors")
