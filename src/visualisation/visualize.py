import os
import matplotlib.pyplot as plt
import calendar
from settings import PROCESSED_PATH, PROCESSED_APPS_PATH, REPORTS_PATH
from utils import file_utils


def show_apps_sum_revenue(count=3, weekday=0, time_range=(0, 23)):
    apps = get_best_apps(count, weekday, time_range)
    fig, ax = plt.subplots()
    day_name = calendar.day_name[weekday]

    for app in apps:
        ax.plot(app['hours'], app['revenue_per_min'], 'o', label=app['name'])

    sum_revenue = int(sum([sum(app['revenue']) for app in apps]))
    ax.set_title(''.join([
        'mean revenue per min',
        day_name, ', from ', str(time_range[0]), ':00 to ', str(time_range[1]),
        ':00 count-', str(count),
        ', old sum =', str(sum_revenue)
    ]))
    ax.legend()

    plt.savefig(''.join([REPORTS_PATH, str(weekday), ' ', day_name, ' ', 'count-', str(count), '.png']))
    plt.show()
    return apps


def get_best_apps(count, weekday, time_range):
    apps = get_apps_sum_revenue(weekday)

    best_apps = {}
    for app in apps:
        for index, hour in enumerate(app['hours']):
            if time_range[0] <= hour and hour <= time_range[1]:
                revenue_per_min = app['revenue_per_min'][index]
                if not hour in best_apps:
                    best_apps[hour] = []

                best_apps[hour].append({
                    'revenue_per_min': revenue_per_min,
                    'name': app['name'],
                    'revenue': app['revenue'][index]
                })

                if len(best_apps[hour]) > count:
                    min_revenue_app = min(best_apps[hour], key=lambda x: x['revenue_per_min'])
                    best_apps[hour].remove(min_revenue_app)

    plot_data = {}
    for key in best_apps.keys():
        for index, app in enumerate(best_apps[key]):
            if app['name'] not in plot_data:
                plot_data[app['name']] = {'hours': [], 'revenue': [], 'revenue_per_min': [], 'name': app['name']}
            plot_data[app['name']]['hours'].append(key)
            plot_data[app['name']]['revenue'].append(app['revenue'])
            plot_data[app['name']]['revenue_per_min'].append(app['revenue_per_min'])

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
    sum_full_revenue = {}
    sum_revenue_per_min = {}
    plot_data = {
        'hours': [],
        'revenue': [],
        'revenue_per_min': []
    }

    for index, el in enumerate(data['Revenue']):
        hour = int(data['Hours'][index])
        duration = data['Duration'][index]
        revenue = data['Revenue'][index]
        if not hour in sum_full_revenue:
            sum_full_revenue[hour] = 0
            sum_revenue_per_min[hour] = []
        sum_full_revenue[hour] += revenue
        sum_revenue_per_min[hour].append(revenue / (duration or 1))

    for hour in sum_revenue_per_min:
        sum_revenue_per_min[hour] = mean(sum_revenue_per_min[hour])

    for hour in sum_full_revenue:
        plot_data['hours'].append(hour)
        plot_data['revenue'].append(sum_full_revenue[hour])
        plot_data['revenue_per_min'].append(sum_revenue_per_min[hour])

    return {
        'hours': plot_data['hours'],
        'revenue': plot_data['revenue'],
        'revenue_per_min': plot_data['revenue_per_min'],
        'name': file_name
    }


def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)
