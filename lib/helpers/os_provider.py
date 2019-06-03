import os


def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


def ensure_db(file_name):
    if not os.path.exists(file_name):
        f = open(file_name, 'w')
        f.close()


def check_files_exist(dir_path):
    try:
        _ = os.path.isfile("%s/Products.csv" % dir_path)
        _ = os.path.isfile("%s/Nutrients.csv" % dir_path)
        _ = os.path.isfile("%s/Serving_size.csv" % dir_path)
        print("files found...")
    except OSError:
        print("Files Not found in ../raw_data dir")
        quit()
