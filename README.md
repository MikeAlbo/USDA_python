# USDA CSV TO SQLITE PARSERS
The current source files for this project are deprecated but are still available. The information within the files should still be accurate but it is not recent. The tables are matched using the **NDB_number** provided in each file. There are rows in both the Serving_size.csv and Nutrients.csv file that do not exist in the Products.csv and vice versa, the parsers and cleanup scripts should resolve all discrepancies. The **future version with API access** should resolve all DB missing data issues.


to add:
* partial lookup for product name (return multiple results)
* multiple return values for upc lookup ( will need to add new table for upc, will fix  insert errors)
* add query as search into main application  


**Instructions**
---
1. Download the CSV files from [USDA data source](https://ndb.nal.usda.gov/ndb/)
2. save the files (Products.csv, Nutrients.csv, Serving_size.csv) in **../raw_data/**
3. Run the USDA_data_parser file (can select which parser to run, or run all)
5. use usda_db_query to perform searches 

**must run "product" parser first or "all" first**

## SQLite DB version w/o API access
The first version will store the products with non-matching data in the Nutrients and Serving Size tables
in the main database. The lookup functions will search that table first and return "NO DATA" for any missing data.

## SQLite DB version with API access
v2 will incorporate the food data API and will call that API if the product data does not
exist in the DB. Therefore we can remove the second products table from the DB reducing its initial size.


## things left to add

* USDA API integration
* add option to drop tables/ single tables
* add prompt to use existing db, delete db, new db 
* CREATE time class and use it to log parse times, print logs
* CREATE error class, capture and log errors, print logs
* change parser complete value to false when table is dropped