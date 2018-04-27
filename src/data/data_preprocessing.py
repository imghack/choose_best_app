import csv

READ_ROOT_FOLDER = '../../data/raw/'
WRITE_ROOT_FOLDER = '../../data/processed/'
FILES = ['apps.csv', 'link_data.csv', 'orders.csv']

docs = {}


def read():
    for file_name in FILES:
        file_path = READ_ROOT_FOLDER + file_name
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            docs[file_name] = list(reader)
    return docs


def write():
    for file_name in FILES:
        file_path = WRITE_ROOT_FOLDER + file_name

        file = open(file_path, 'w')
        with file:
            writer = csv.writer(file)
            writer.writerows(docs[file_name])


if __name__ == '__main__':
    read()
    write()
