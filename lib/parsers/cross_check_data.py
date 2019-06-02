def main():

    from lib.sql.usda_db import usda_db

    product_ids = set(usda_db.sel_rtn_row('''SELECT product_id FROM Products'''))
    nutrition_ids = set(usda_db.sel_rtn_row('''SELECT product_id FROM Nutrients'''))
    serving_sizes_ids = set(usda_db.sel_rtn_row('''SELECT product_id FROM Serving_sizes'''))

    bad_count = 0
    count_down = len(product_ids)
    product_rows_deleted = 0
    rows_not_deleted = 0

    def delete_row(product_id):
        try:
            usda_db.db.execute_sql('''DELETE FROM Products WHERE product_id=?''', (product_id,))
            if product_rows_deleted % 10 == 0:
                usda_db.db.commit()
            return 0
        except:
            print("row not removed")
            return 1

    print("retrieving data...")

    for p_id in product_ids:
        count_down -= 1
        if p_id in nutrition_ids and p_id in serving_sizes_ids:
            print(count_down)
            continue
        else:
            bad_count += 1
            product_rows_deleted += 1
            rows_not_deleted += delete_row(p_id[0])

    usda_db.db.commit()
    print("\n\n----- done -----\n\n")
    print("bad: ", bad_count)
    print("rows deleted:", product_rows_deleted)
    print("rows needed deleted but not: ", rows_not_deleted)
