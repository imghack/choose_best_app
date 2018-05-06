import os
import matplotlib.pyplot as plt
from settings import PROCESSED_PATH, PROCESSED_APPS_PATH, REPORTS_PATH
from utils import file_utils

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


def show_apps_sum_revenue(count=None):
    if count:
        apps = get_best_apps(count)
    else:
        apps = get_apps_sum_revenue()

    fig, ax = plt.subplots()

    for app in apps:
        ax.plot(app['hours'], app['values'], 'o', label=app['name'])
        ax.legend()

    plt.savefig(''.join([REPORTS_PATH, str(count), '.png']))
    plt.show()
    return apps


def get_apps_sum_revenue():
    files = os.listdir(PROCESSED_APPS_PATH)
    property1 = 'Revenue'
    property2 = 'Duration'
    apps = []

    for file in files:
        sumDelta = {}
        plot_data = {
            'hours': [],
            'values': []
        }

        app_path = ''.join([PROCESSED_APPS_PATH, file])
        data = file_utils.fetch_data(app_path)

        # delta = [
        #     data[property1][index] / (data[property2][index] or 0.01)
        #     for index, el in enumerate(data[property1])
        # ]

        for index, el in enumerate(data[property1]):
            hour = int(data['Hours'][index])
            revenue = data[property1][index]
            if not hour in sumDelta:
                sumDelta[hour] = 0
            sumDelta[hour] += revenue

        for hour in sorted(sumDelta):
            plot_data['hours'].append(hour)
            plot_data['values'].append(sumDelta[hour])

        apps.append({'hours': plot_data['hours'], 'values': plot_data['values'], 'name': file})

    return apps


def get_best_apps(count):
    apps = get_apps_sum_revenue()

    best_apps = {}
    for app in apps:
        for index, hour in enumerate(app['hours']):
            val = app['values'][index]
            if not hour in best_apps:
                best_apps[hour] = []

            if len(best_apps[hour]) < count:
                best_apps[hour].append({'val': val, 'name': app['name']})
            else:
                best_apps[hour].append({'val': val, 'name': app['name']})
                min_revenue_app = min(best_apps[hour], key=lambda x: x['val'])

                best_apps[hour].remove(min_revenue_app)

    plot_data = {}
    for key in best_apps.keys():
        for index, app in enumerate(best_apps[key]):
            if app['name'] not in plot_data:
                plot_data[app['name']] = {'hours': [], 'values': [], 'name': app['name']}
            plot_data[app['name']]['hours'].append(key)
            plot_data[app['name']]['values'].append(app['val'])

    return [plot_data[key] for key in plot_data.keys()]

# def show_apps_medium_revenue_per_hour():
#     fig, ax = plt.subplots()
#     files = os.listdir(PROCESSED_APPS_PATH)
#     property1 = 'Revenue'
#     property2 = 'Duration'
#     max_revenues = []
#
#     for file in files:
#         sumDelta = {}
#         plot_data = {
#             'hours': [],
#             'values': []
#         }
#
#         app_path = ''.join([PROCESSED_APPS_PATH, file])
#         data = file_utils.fetch_data(app_path)
#
#         delta = [
#             data[property1][index] / (data[property2][index] or 0.01)
#             for index, el in enumerate(data[property1])
#         ]
#
#         for index, el in enumerate(data[property1]):
#             hour = int(data['Hours'][index])
#             # revenue = data[property1][index]
#             if not hour in sumDelta:
#                 sumDelta[hour] = 0
#             sumDelta[hour] += delta[index]
#
#         for hour in sorted(sumDelta):
#             plot_data['hours'].append(hour)
#             plot_data['values'].append(sumDelta[hour])
#
#         ax.plot(plot_data['hours'], plot_data['values'], 'o', label=file)
#         ax.legend()
#
#     plt.show()

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
