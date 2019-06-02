import time

import helpers.helpers as helpers
import helpers.user_input as user_input
from lib.create_tables import create_tables
from drop_tables import drop_all_tables
from parsers.product_table_parser import main as prod_parser
from parsers.nutrition_table_parser import main as nutrient_parser
from parsers.serving_table_parser import main as serving_parser


source_path = "../raw_data"
db_name = "USDA1.sqlite"
db_path = "../db/"
possible_search_options = ["product_parse", "nutrient_parse", "serving_parse", "full"]
p_parser_ran = False
n_parser_ran = False
s_parser_ran = False
current_time = 0

print("USDA csv data should be located in %s" % source_path)
user_input.user_ready()

helpers.check_files_exist(source_path)

start_time = time.process_time()

user_input_parse_type = user_input.user_select_parse_type(possible_search_options)

db_connection = helpers.make_db_connection(db_path, db_name)
cur = db_connection.cursor()

# todo: remove! for testing
drop_all_tables(cur)
create_tables(cur)
helpers.init_parser_complete_table(cur, db_connection)
# completed_parsers = helpers.completed_parsers(cur)
# helpers.parser_ran_complete(cur, db_connection, "product_parser")
# print(helpers.completed_parsers(cur)["p_p"])
# quit()

if user_input_parse_type == "full" or user_input_parse_type == "product_parse":
    prod_parser(source_path + "/Products.csv", cur, db_connection)
    p_parser_ran = True
    helpers.parser_ran_complete(cur, db_connection, "product_parser")
    current_time = time.process_time() - start_time
    print("\n____________________\n Products parse time %.1f ms \n" % (current_time * 1000))

if user_input_parse_type == "full" or user_input_parse_type == "nutrient_parse":
    if helpers.completed_parsers(cur)["p_p"] is False:
        print("product parser needs to run first")
        quit()
    nutrient_parser(source_path + "/Nutrients.csv", cur, db_connection)
    n_parser_ran = True
    helpers.parser_ran_complete(cur, db_connection, "nutrition_parser")
    current_time = time.process_time() - start_time
    print("\n____________________\n Nutrients parse time %.1f ms \n" % (current_time * 1000))

if user_input_parse_type == "full" or user_input_parse_type == "serving_parse":
    if helpers.completed_parsers(cur)["p_p"] is False:
        print("product parser needs to run first")
        quit()
    serving_parser(source_path + "/Serving_size.csv", cur, db_connection)
    s_parser_ran = True
    helpers.parser_ran_complete(cur, db_connection, "serving_parser")
    current_time = time.process_time() - start_time
    print("\n____________________\n Serving size parse time %.1f ms \n" % (current_time * 1000))

# print("user input:", user_input_parse_type)
# print(helpers.completed_parsers(cur))
cur.close()





