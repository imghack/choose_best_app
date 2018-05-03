import os
import csv
from collections import defaultdict
import matplotlib.pyplot as plt

PATH = '../../data/processed/'
APPS_PATH = ''.join([PATH, 'apps/'])


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


# all_apps_path = ''.join([PATH, 'apps.csv'])
# data = fetch_data(all_apps_path)


# fig, ax = plt.subplots()
# ax.set_ylabel('duration')
# ax.set_xlabel('hours')
# ax.plot(data['Time'], data['Duration'], 'o')
#
# count = 600
# ax.plot(data['Time'][:count], data['Duration'][:count], 'o')
# ax.set_title('Duration when people are using apps')
#
# fig1, ax1 = plt.subplots()
# ax1.set_ylabel('revenue')
# ax1.set_xlabel('hours')
# ax1.plot(data['Time'], data['Revenue'], 'o')
#
# count = 600
# ax1.plot(data['Time'][:count], data['Revenue'][:count], 'o')
# ax1.set_title('Revenue')

# fig, ax = plt.subplots()
# ax.set_ylabel('duration')
# ax.set_xlabel('hours')
#
#

fig, ax = plt.subplots()
files = os.listdir(APPS_PATH)
for file in files:
    app_path = ''.join([APPS_PATH, file])
    data = fetch_data(app_path)
    ax.plot(data['Time'], data['Duration'], 'o')

fig, ax = plt.subplots()
files = os.listdir(APPS_PATH)
for file in files:
    app_path = ''.join([APPS_PATH, file])
    data = fetch_data(app_path)
    ax.plot(data['Time'], data['Revenue'], 'o')

plt.show()
