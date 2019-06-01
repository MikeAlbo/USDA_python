import os


def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


def ensure_db(file_name):
    if not os.path.exists(file_name):
        f = open(file_name, 'w')
        f.close()
