import csv
from collections import defaultdict
import matplotlib.pyplot as plt

data = defaultdict(list)

with open('../../data/processed/apps.csv', 'r') as f:
    reader = csv.DictReader(f)  # read rows into a dictionary format
    for row in reader:  # read a row as {column1: value1, column2: value2,...}
        for (k, v) in row.items():  # go over each column name and value
            if k == 'Time' or k == 'Duration':
                v = float(v)
            data[k].append(v)

fig, ax = plt.subplots()
count = 600
ax.set_ylabel('duration')
ax.set_xlabel('hours')
ax.plot(data['Time'], data['Duration'], 'o')
ax.plot(data['Time'][:count], data['Duration'][:count], 'o')
ax.set_title('Duration when people are using apps')
plt.show()
