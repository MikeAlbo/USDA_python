# USDA CSV TO SQLITE PARSERS

The current source files for this project are deprecated but are still available. The information within the files should still be accurate but it is not recent. The tables are matched using the **NDB_number** provided in each file. There are rows in both the Serving_size.csv and Nutrients.csv file that do not exist in the Products.csv and vice versa, the parsers and cleanup scripts should resolve all discrepancies. The **future version with API access** should resolve all DB missing data issues.

**Instructions**
---
1. Download the CSV files from [USDA data source](https://ndb.nal.usda.gov/ndb/)
2. save the files (Products.csv, Nutrients.csv, Serving_size.csv) in **../raw_data/**
3. Run the USDA_data_parser file (currently separate files, run usda_product_table... first)
4. Run cross_check_data.py   ***--takes about an hour!--***
5. use usda_db_query to perform searches 

**must run usda_products_table_parser.py first**

## SQLite DB version w/o API access
The first version will store the products with non-matching data in the Nutrients and Serving Size tables
in the main database. The lookup functions will search that table first and return "NO DATA" for any missing data.

## SQLite DB version with API access
v2 will incorporate the food data API and will call that API if the product data does not
exist in the DB. Therefore we can remove the second products table from the DB reducing its initial size.


## things left to add
* auto-generate a db dir if one does not exist 
* use flag/ argument to name/ increment database
* refinement of user flow for parsing data
* arguments to be added to parser and lookup scripts - delete tables, readme
* combining all parsers into on script
* add a table that contains bool (1 / 0) values if a parser has been run
* lookup functions check to make sure all parsers have been run 