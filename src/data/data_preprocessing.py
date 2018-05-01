import csv
from utils.time_utils import append_time_duration

READ_ROOT_FOLDER = '../../data/raw/'
WRITE_ROOT_FOLDER = '../../data/processed/'
FILES = ['apps.csv']
SUB_FILES = ['link_data.csv', 'orders.csv']


def read():
    apps = []
    link_data = {}
    orders = {}

    with open(READ_ROOT_FOLDER + 'link_data.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            link_data[row['ApplicationID'].lower()] = row

    with open(READ_ROOT_FOLDER + 'orders.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            orders[row['SessionId'].lower()] = row

    with open(READ_ROOT_FOLDER + 'apps.csv', 'r') as f:
        reader = csv.reader(f)
        apps = list(reader)

    return apps, link_data, orders


def write(apps):
    file = open(WRITE_ROOT_FOLDER + 'apps.csv', 'w')
    with file:
        writer = csv.writer(file)
        writer.writerows(apps)


# TODO: you can have few session id's with difference revenue ... add time to get correct revenue
def append_revenue(apps, link_data, orders):
    apps[0].append('Revenue')

    counter = 0

    for app in apps[1:]:
        try:
            link = link_data[app[3]]
            sess_id = link['SessionID'].lower()
            revenue = orders[sess_id]['Revenue']
            app.append(round(float(revenue), 2))
        except:
            apps.remove(app)
            counter += 1

    print('MISSED ITEMS ', counter)


if __name__ == '__main__':
    apps, link_data, orders = read()

    print(len(apps))
    print(len(link_data.keys()))
    print(len(orders.keys()))
    append_time_duration(apps, start_time_index=1, end_time_index=2)
    append_revenue(apps, link_data, orders)

    write(apps)
