import csv
from collections import defaultdict
import matplotlib.pyplot as plt

data = defaultdict(list)

PATH = '../../data/processed/apps.csv'

with open(PATH, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        for (k, v) in row.items():
            if k == 'Time' or \
                    k == 'Duration' or \
                    k == 'Revenue':
                v = float(v)
            data[k].append(v)

fig, ax = plt.subplots()
ax.set_ylabel('duration')
ax.set_xlabel('hours')
ax.plot(data['Time'], data['Duration'], 'o')

count = 600
ax.plot(data['Time'][:count], data['Duration'][:count], 'o')
ax.set_title('Duration when people are using apps')

fig1, ax1 = plt.subplots()
ax1.set_ylabel('revenue')
ax1.set_xlabel('hours')
ax1.plot(data['Time'], data['Revenue'], 'o')

count = 600
ax1.plot(data['Time'][:count], data['Revenue'][:count], 'o')
ax1.set_title('Revenue')

plt.show()
