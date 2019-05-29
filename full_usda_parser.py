import csv
import sqlite3
import time
import os
import sys

import lib.helpers as helpers
import lib.user_input as user_input
from lib.create_tables import create_tables
from lib.drop_tables import drop_all_tables
from lib.product_table_parser import main as prod_parser


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

if user_input_parse_type == "full" or user_input_parse_type == "product_parser":
    prod_parser(source_path + "/Products.csv", cur, db_connection)
    p_parser_ran = True
    current_time = time.process_time() - start_time
    print("\n____________________\n Products parse time %.1f ms \n" % (current_time * 1000))


cur.close()





