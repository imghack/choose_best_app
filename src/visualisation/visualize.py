import os
import matplotlib.pyplot as plt
import calendar
from settings import PROCESSED_PATH, PROCESSED_APPS_PATH, REPORTS_PATH
from utils import file_utils


def show_apps_sum_revenue(count=3, weekday=0):
    apps = get_best_apps(count, weekday)
    fig, ax = plt.subplots()

    for app in apps:
        ax.plot(app['hours'], app['values'], 'o', label=app['name'])
        ax.legend()

    day_name = calendar.day_name[weekday]
    plt.savefig(''.join([REPORTS_PATH, str(weekday), ' ', day_name, ' ', 'count-', str(count), '.png']))
    plt.show()
    return apps


def get_best_apps(count, weekday):
    apps = get_apps_sum_revenue(weekday)

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


def get_apps_sum_revenue(weekday_index):
    files = os.listdir(PROCESSED_APPS_PATH)
    apps = []

    for file in files:
        app_path = ''.join([PROCESSED_APPS_PATH, file])
        data = file_utils.fetch_data(app_path)
        weekdays_data = {}

        # for weekday in range(0, 7):
        for index, weekday in enumerate(data['Weekday']):
            weekday = int(weekday)
            if weekday not in weekdays_data:
                weekdays_data[weekday] = {
                    'Duration': [],
                    'Revenue': [],
                    'Hours': []
                }
            weekdays_data[weekday]['Duration'].append(data['Duration'][index])
            weekdays_data[weekday]['Revenue'].append(data['Revenue'][index])
            weekdays_data[weekday]['Hours'].append(data['Hours'][index])

        apps.append(sum_revenue(weekdays_data[weekday_index], file))

    return apps


def sum_revenue(data, file_name):
    revenue_key = 'Revenue'
    sum_revenue = {}
    plot_data = {
        'hours': [],
        'values': []
    }

    for index, el in enumerate(data[revenue_key]):
        hour = int(data['Hours'][index])
        revenue = data[revenue_key][index]
        if not hour in sum_revenue:
            sum_revenue[hour] = 0
        sum_revenue[hour] += revenue

    for hour in sorted(sum_revenue):
        plot_data['hours'].append(hour)
        plot_data['values'].append(sum_revenue[hour])

    return {'hours': plot_data['hours'], 'values': plot_data['values'], 'name': file_name}
