import csv
from utils.time_utils import append_time_duration

READ_ROOT_FOLDER = '../../data/raw/'
WRITE_ROOT_FOLDER = '../../data/processed/'
FILES = ['apps.csv', 'link_data.csv', 'orders.csv']


def read():
    documents = {}
    for file_name in FILES:
        file_path = READ_ROOT_FOLDER + file_name
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            documents[file_name] = list(reader)
    return documents


def write(documents):
    for file_name in FILES:
        file_path = WRITE_ROOT_FOLDER + file_name

        file = open(file_path, 'w')
        with file:
            writer = csv.writer(file)
            writer.writerows(documents[file_name])


if __name__ == '__main__':
    docs = read()
    append_time_duration(docs['apps.csv'], start_time_index=1, end_time_index=2)
    write(docs)
