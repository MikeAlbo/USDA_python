import sqlite3
import time

start_time = time.process_time()


def print_product(prod):
    print("___________________________\n")
    print("%s" % prod[2])
    print("NDB#: %s" % prod[1])
    print("UPC: %s" % prod[3])
    print("Manufacture: %s" % prod[4])
    print("Ingredients: \n %s" % prod[5])


def get_product(upc, search_type):
    cur.execute('''
    SELECT 
        product_id, ndb_number,long_name,gtin_upc, 
        Manufactures.manufacture_name, 
        ingredients.ingredients 
        FROM Products 
        INNER JOIN Manufactures on  Manufactures.manufacture_id = Products.manufacture_id
        INNER JOIN ingredients on ingredients.ingredient_id = Products.ingredients_id
        WHERE %s=?
        ''' % search_type, (upc,))
    p = cur.fetchone()
    print_product(p)
    return p[0]


def print_serving_size(prod):
    print("___________________________\n")
    print("serving size %s" % prod[0], prod[1])
    print("family serving size: %s" % prod[2], prod[3])


def get_serving_size(p_id):
    cur.execute('''
    SELECT 
        serving_size,
        Units.unit,
        household_serving_size,
        Household_uom.unit 
        FROM Serving_sizes 
        INNER JOIN Units on  Units.uom_id = Serving_sizes.serving_size_uom
        INNER JOIN Household_uom on  Household_uom.household_uom_id = Serving_sizes.household_serving_size_uom
        WHERE product_id=?
        ''', (p_id,))
    s = cur.fetchone()
    print_serving_size(s)


def print_nutrients(nutrients):
    print("___________________________\n")
    print("Nutrient | Amount | Derivation Code")
    print("===================================")
    for v in nutrients:
        print(v[0], "-", v[1], v[2], " | ", v[3])


def get_nutrition(p_id):
    cur.execute('''
    SELECT 
        NutrientCodes.nutrient_name,
        output_value, 
        Units.unit,
        Derivation.derivation_code
        FROM Nutrients 
        INNER JOIN NutrientCodes on  NutrientCodes.nutrient_code = Nutrients.nutrient_code
        INNER JOIN Units on  Units.uom_id = Nutrients.uom_id
        INNER JOIN Derivation on Derivation.derivation_id = Nutrients.derivation_id
        WHERE product_id=?
    ''', (p_id,))
    n = cur.fetchall()
    print_nutrients(n)


user_input = 0
user_input_search_type = None
possible_search_options = ['long_name', "upc", "ndb_number"]


print("-- Product Lookup --")
try:
    temp = input("select type %s: " % possible_search_options)
    if temp in possible_search_options:
        user_input_search_type = temp
except ValueError:
    print("must select one of ", possible_search_options)
    quit()

db_connection = None

try:
    db_connection = sqlite3.connect('file:../db/USDA2.sqlite?mode=rw', uri=True)
except sqlite3.Error:
    print("USDA.sqlite does not exist in ../db/ folder")

cur = db_connection.cursor()


try:
    user_input = input("Enter %s: " % user_input_search_type)
    if user_input_search_type == "upc":
        user_input_search_type = "gtin_upc"
    if user_input_search_type != "long_name":
        user_input = int(user_input)
except ValueError:
    print('" %s ", is an invalid input' % user_input)
    quit()

try:
    p_id = get_product(user_input, user_input_search_type)
    get_serving_size(p_id)
    get_nutrition(p_id)
except TypeError:
    print("lookup failed")


db_connection.close()
elapsed_time = time.process_time() - start_time
print("\n____________________\n Query time %.1f ms \n" % (elapsed_time * 1000))

