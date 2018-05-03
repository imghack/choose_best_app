import os
import csv
import dateutil.parser
import shutil
from utils.time_utils import append_time_duration

READ_ROOT_FOLDER = '../../data/raw/'
WRITE_ROOT_FOLDER = '../../data/processed/'


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
            if not (row['SessionId'].lower() in orders.keys()):
                orders[row['SessionId'].lower()] = []
            orders[row['SessionId'].lower()].append(row)

    with open(READ_ROOT_FOLDER + 'apps.csv', 'r') as f:
        reader = csv.reader(f)
        apps = list(reader)

    return apps, link_data, orders


def write(apps):
    file = open(WRITE_ROOT_FOLDER + 'apps.csv', 'w')
    with file:
        writer = csv.writer(file)
        writer.writerows(apps)


def write_files_by_app_name(apps):
    reset_apps_folder()
    app_names = []
    for app in apps[1:]:
        app_name = app[0].split(".")[2]
        path = "".join([WRITE_ROOT_FOLDER, "apps/", app_name, ".csv"])

        if app_name not in app_names:
            app_names.append(app_name)
            write_row(path, apps[0])
        write_row(path, app)


# TODO : helper
def write_row(path, row):
    file = open(path, 'a')
    with file:
        writer = csv.writer(file)
        writer.writerow(row)


# TODO : helper
def reset_apps_folder():
    apps_path = "".join([WRITE_ROOT_FOLDER, "apps/"])
    if os.path.exists(apps_path):
        shutil.rmtree(apps_path)
    os.mkdir(apps_path)


def append_revenue(apps, link_data, orders):
    apps[0].append('Revenue')

    counter = 0

    for app in apps[1:]:
        try:
            link = link_data[app[3]]
            sess_id = link['SessionID'].lower()
            orders_by_sess_id = orders[sess_id]
            min_delta = None
            best_index = None

            app_time = dateutil.parser.parse(app[1]).replace(tzinfo=None)

            for index, order in enumerate(orders_by_sess_id):
                order_time = dateutil.parser.parse(order['Time'])
                delta = order_time - app_time
                if not min_delta or delta < min_delta:
                    min_delta = delta
                    best_index = index

            revenue = round(float(orders_by_sess_id[best_index]['Revenue']), 2)
            app.append(revenue)
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
    print('added Time duration')
    append_revenue(apps, link_data, orders)
    print('added revenue')
    write(apps)
    write_files_by_app_name(apps)
