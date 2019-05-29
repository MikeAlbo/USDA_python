import csv

count = 0

print("files must be located in raw_data")
file_to_test = "Products.csv"
path = "../raw_data/%s" % file_to_test
upc_list = list()
nbd_list = list()
upc_errors = 0
nbd_errors = 0

with open(path) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    for row in csv_reader:
        if row[0] not in nbd_list:
            nbd_list.append(row[0])
        else:
            nbd_errors += 1

        if row[3] not in upc_list:
            upc_list.append(row[3])
        else:
            upc_errors += 1
        count += 1
        print(count)


print(count)
print("upc_list", len(upc_list))
print("nbd_list", len(nbd_list))
print("\n")
print("upc errors", upc_errors)
print("nbd errors", nbd_errors)