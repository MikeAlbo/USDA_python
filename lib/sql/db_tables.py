def get_create_table_list():
    """return the tables to be create as strings"""

    return [
        ''' CREATE TABLE IF NOT EXISTS Products (
            product_id INTEGER PRIMARY KEY, ndb_number INTEGER UNIQUE, long_name INTEGER,
            gtin_upc INTEGER UNIQUE, manufacture_id INTEGER, ingredients_id INTEGER
            )''',
        '''CREATE TABLE IF NOT EXISTS Manufactures (
            manufacture_id INTEGER PRIMARY KEY, manufacture_name TEXT UNIQUE
            )''',
        '''CREATE TABLE IF NOT EXISTS Long_names (
            long_name_id INTEGER PRIMARY KEY, long_name TEXT UNIQUE
            )''',
        '''CREATE TABLE IF NOT EXISTS Ingredients (
            ingredient_id INTEGER PRIMARY KEY, ingredients TEXT UNIQUE
            )''',
        '''CREATE TABLE IF NOT EXISTS Nutrients (
            product_nutrient_id INTEGER PRIMARY KEY, product_id INTEGER, nutrient_code INTEGER, 
            uom_id INTEGER, derivation_id INTEGER, output_value INTEGER
            )''',
        '''CREATE TABLE IF NOT EXISTS Units (
            uom_id INTEGER PRIMARY KEY, unit TEXT UNIQUE
            )''',
        '''CREATE TABLE IF NOT EXISTS Derivation (
            derivation_id INTEGER PRIMARY KEY, derivation_code TEXT UNIQUE
            )''',
        '''CREATE TABLE IF NOT EXISTS Nutrient_codes(
            nutrient_code INTEGER PRIMARY KEY, nutrient_name TEXT UNIQUE
            )''',
        '''CREATE TABLE IF NOT EXISTS Serving_sizes (
            serving_size_id INTEGER PRIMARY KEY, product_id INTEGER, 
            serving_size INTEGER, serving_size_uom INTEGER,
            household_serving_size INTEGER, household_serving_size_uom INTEGER 
            )''',
        '''CREATE TABLE IF NOT EXISTS Household_uom (
            household_uom_id INTEGER PRIMARY KEY, unit TEXT UNIQUE
            )''',
        '''CREATE TABLE IF NOT EXISTS Parsers_ran (
            parser_id INTEGER PRIMARY KEY, 
            product_parser INTEGER, 
            nutrition_parser INTEGER, 
            serving_parser INTEGER
            )'''
    ]


def get_drop_table_list():
    return [
        '''DROP TABLE IF EXISTS Products''',
        '''DROP TABLE IF EXISTS Manufactures''',
        '''DROP TABLE IF EXISTS Ingredients''',
        '''DROP TABLE IF EXISTS Nutrients''',
        '''DROP TABLE IF EXISTS Units''',
        '''DROP TABLE IF EXISTS Derivation''',
        '''DROP TABLE IF EXISTS Nutrient_codes''',
        '''DROP TABLE IF EXISTS Serving_sizes''',
        '''DROP TABLE IF EXISTS Household_uom''',
        '''DROP TABLE IF EXISTS Long_names''',
        '''DROP TABLE IF EXISTS Parsers_ran'''
    ]
