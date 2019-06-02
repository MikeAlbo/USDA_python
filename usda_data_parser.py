import time

import lib.helpers.helpers as helpers
import lib.helpers.user_input as user_input
from lib.parsers.product_table_parser import main as prod_parser
from lib.parsers.nutrition_table_parser import main as nutrient_parser
from lib.parsers.serving_table_parser import main as serving_parser
from lib.sql.usda_db import usda_db


source_path = "../raw_data"
db_name = "USDA_test.sqlite"
db_path = "../db/"
possible_search_options = ["product_parse", "nutrient_parse", "serving_parse", "full"]
current_time = 0

print("USDA csv data should be located in %s" % source_path)
user_input.user_ready()

start_time = time.process_time()

user_input_parse_type = user_input.user_select_parse_type(possible_search_options)

usda_db.init_usda_db(db_path, db_name)
usda_db.db_running()

if user_input_parse_type == "full" or user_input_parse_type == "product_parse":
    prod_parser(source_path + "/Products.csv")
    usda_db.parser_ran_complete("product_parser")
    current_time = time.process_time() - start_time
    print("\n____________________\n Products parse time %.1f ms \n" % (current_time * 1000))
#
# if user_input_parse_type == "full" or user_input_parse_type == "nutrient_parse":
#     if helpers.completed_parsers(cur)["p_p"] is False:
#         print("product parser needs to run first")
#         quit()
#     nutrient_parser(source_path + "/Nutrients.csv", cur, db_connection)
#     helpers.parser_ran_complete(cur, db_connection, "nutrition_parser")
#     current_time = time.process_time() - start_time
#     print("\n____________________\n Nutrients parse time %.1f ms \n" % (current_time * 1000))
#
# if user_input_parse_type == "full" or user_input_parse_type == "serving_parse":
#     if helpers.completed_parsers(cur)["p_p"] is False:
#         print("product parser needs to run first")
#         quit()
#     serving_parser(source_path + "/Serving_size.csv", cur, db_connection)
#     helpers.parser_ran_complete(cur, db_connection, "serving_parser")
#     current_time = time.process_time() - start_time
#     print("\n____________________\n Serving size parse time %.1f ms \n" % (current_time * 1000))
#
print("user input:", user_input_parse_type)
print(usda_db.completed_parsers())
usda_db.db.close_connection()





