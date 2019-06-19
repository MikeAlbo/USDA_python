import time

import lib.helpers.helpers as helpers
import lib.helpers.user_input as user_input
from lib.parsers.product_table_parser import main as prod_parser
from lib.parsers.nutrition_table_parser import main as nutrient_parser
from lib.parsers.serving_table_parser import main as serving_parser
from lib.parsers.cross_check_data import main as cross_check
from lib.sql.usda_db import usda_db
from lib.helpers.os_provider import check_files_exist


source_path = "../raw_data"
db_name = "USDA_test.sqlite"
db_path = "../db/"
possible_search_options = ["product_parse", "nutrient_parse", "serving_parse", "full", "clean"]
current_time = 0

print("USDA csv data should be located in %s" % source_path)
user_input.user_ready()

check_files_exist(db_path)

user_input_parse_type = user_input.welcome(possible_search_options)

start_time = time.process_time()

usda_db.init_usda_db(db_path, db_name)
usda_db.db_running()

if user_input_parse_type == "full" or user_input_parse_type == "product_parse":
    prod_parser(source_path + "/Products.csv")
    usda_db.parser_ran_complete("product_parser")
    current_time = time.process_time() - start_time  # todo: fix time, create class
    print("\n____________________\n Products parse time %.1f ms \n" % (current_time * 1000))

if user_input_parse_type == "full" or user_input_parse_type == "nutrient_parse":
    helpers.product_parser_check()
    nutrient_parser(source_path + "/Nutrients.csv")
    usda_db.parser_ran_complete("nutrition_parser")
    current_time = time.process_time() - start_time
    print("\n____________________\n Nutrients parse time %.1f ms \n" % (current_time * 1000))

if user_input_parse_type == "full" or user_input_parse_type == "serving_parse":
    helpers.product_parser_check()
    serving_parser(source_path + "/Serving_size.csv")
    usda_db.parser_ran_complete("serving_parser")
    current_time = time.process_time() - start_time
    print("\n____________________\n Serving size parse time %.1f ms \n" % (current_time * 1000))

if user_input_parse_type == "full" or user_input_parse_type == "clean":
    helpers.all_parsers_complete()
    print("Parsers complete, proceed with Product table cleanup?")
    user_input.user_ready()
    cross_check()
    current_time = time.process_time() - start_time
    print("\n____________________\n Serving size parse time %.1f ms \n" % (current_time * 1000))


print("user input:", user_input_parse_type)
print(usda_db.completed_parsers())
usda_db.db.close_connection()





