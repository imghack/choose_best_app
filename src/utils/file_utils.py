import os
import csv
import shutil
from settings import RAW_PATH, PROCESSED_PATH, PROCESSED_APPS_PATH
from collections import defaultdict


def fetch_data(path):
    with open(path, 'r') as f:
        data = defaultdict(list)
        reader = csv.DictReader(f)
        for row in reader:
            for (k, v) in row.items():
                if k == 'Time' or \
                        k == 'Duration' or \
                        k == 'Revenue':
                    v = float(v)
                data[k].append(v)

    return data


def read_raw_data():
    apps = []
    link_data = {}
    orders = {}

    with open(RAW_PATH + 'link_data.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            link_data[row['ApplicationID'].lower()] = row

    with open(RAW_PATH + 'orders.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not (row['SessionId'].lower() in orders.keys()):
                orders[row['SessionId'].lower()] = []
            orders[row['SessionId'].lower()].append(row)

    with open(RAW_PATH + 'apps.csv', 'r') as f:
        reader = csv.reader(f)
        apps = list(reader)

    return apps, link_data, orders


def write(apps):
    file = open(PROCESSED_PATH + 'apps.csv', 'w')
    with file:
        writer = csv.writer(file)
        writer.writerows(apps)


def write_files_by_app_name(apps):
    reset_apps_folder()
    app_names = []
    for app in apps[1:]:
        app_name = app[0].split(".")[2]
        path = "".join([PROCESSED_APPS_PATH, app_name, ".csv"])
        if app_name not in app_names:
            app_names.append(app_name)
            write_row(path, apps[0])
        write_row(path, app)


def write_row(path, row):
    file = open(path, 'a')
    with file:
        writer = csv.writer(file)
        writer.writerow(row)


def reset_apps_folder():
    apps_path = PROCESSED_APPS_PATH
    if os.path.exists(apps_path):
        shutil.rmtree(apps_path)
    os.mkdir(apps_path)
