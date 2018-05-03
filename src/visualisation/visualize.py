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


all_apps_path = ''.join([PATH, 'apps.csv'])
data = fetch_data(all_apps_path)
# show all and random and random 600 apps
fig, ax = plt.subplots()
ax.plot(data['Time'], data['Duration'], 'o')
count = 600
ax.plot(data['Time'][:count], data['Duration'][:count], 'o')

# show all and random and random 600 apps
fig, ax = plt.subplots()
ax.plot(data['Time'], data['Revenue'], 'o')
count = 600
ax.plot(data['Time'][:count], data['Revenue'][:count], 'o')

# show apps by app name
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
