import os
import matplotlib.pyplot as plt
from settings import PROCESSED_PATH, PROCESSED_APPS_PATH
from utils import file_utils


def show_data_by_property(data, property, count):

    fig, ax = plt.subplots()

    if count:
        ax.plot(data['Time'][:count], data[property][:count], 'o')
    else:
        ax.plot(data['Time'], data[property], 'o')


def show_apps_by_property(property, decrease_multiplayer):
    fig, ax = plt.subplots()
    files = os.listdir(PROCESSED_APPS_PATH)

    for file in files:
        app_path = ''.join([PROCESSED_APPS_PATH, file])
        data = file_utils.fetch_data(app_path)
        size = int(len(data['Time']) * decrease_multiplayer)
        ax.plot(data['Time'][:size], data[property][:size], 'o', label=file)
        ax.legend()


def show_apps_difference_by_properties(property1, property2, decrease_multiplayer):
    fig, ax = plt.subplots()
    files = os.listdir(PROCESSED_APPS_PATH)

    for file in files:
        app_path = ''.join([PROCESSED_APPS_PATH, file])
        data = file_utils.fetch_data(app_path)
        size = int(len(data['Time']) * decrease_multiplayer)
        delta = [
            data[property1][index] / (data[property2][index] or 0.01)
            for index, el in enumerate(data[property1])
        ]
        ax.plot(data['Time'][:size], delta[:size], 'o', label=file)
        ax.legend()


def show_apps_max_revenue():
    fig, ax = plt.subplots()
    files = os.listdir(PROCESSED_APPS_PATH)
    property1 = 'Revenue'
    property2 = 'Duration'

    for file in files:
        sumDelta = {}
        plot_data = {
            'hours': [],
            'values': []
        }

        app_path = ''.join([PROCESSED_APPS_PATH, file])
        data = file_utils.fetch_data(app_path)
        delta = [
            data[property1][index] / (data[property2][index] or 0.01)
            for index, el in enumerate(data[property1])
        ]
        for index, el in enumerate(data[property1]):
            hour = int(data['Hours'][index])
            revenue = data[property1][index]
            if not hour in sumDelta:
                sumDelta[hour] = 0
            sumDelta[hour] += revenue

        for hour in sorted(sumDelta):
            plot_data['hours'].append(hour)
            plot_data['values'].append(sumDelta[hour])

        ax.plot(plot_data['hours'], plot_data['values'], 'o', label=file)
        ax.legend()

    plt.show()


# if __name__ == '__main__':
# all_apps_path = ''.join([PATH, 'apps.csv'])
# data = fetch_data(all_apps_path)

# show_data_by_property(data, 'Duration', 600)
# show_data_by_property(data, 'Revenue', 600)
# show_apps_by_property('Duration', 1)
# show_apps_by_property('Revenue', 1)
# show_apps_by_property('Duration', 1 / 200)
# show_apps_by_property('Revenue', 1 / 200)
# show_apps_difference_by_properties('Revenue', 'Duration', 1)
# show_apps_max_revenue()
