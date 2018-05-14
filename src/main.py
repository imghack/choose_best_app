from data import preprocess
from utils import file_utils
from visualisation import visualize


def prepare_data():
    apps, link_data, orders = file_utils.read_raw_data()
    print('apps count ', len(apps))
    preprocess.append_time_duration(apps, start_time_index=1, end_time_index=2)
    print('added Time duration')
    preprocess.append_revenue(apps, link_data, orders)
    print('added revenue')
    preprocess.append_time_in_hours(apps, start_time_index=1)
    print('added Time in hours')
    preprocess.append_time_in_days(apps, start_time_index=1)
    print('added Time in days')
    file_utils.write(apps)
    file_utils.write_files_by_app_name(apps)
    print('finished data preprocessing!')


def show_best_apps(count):
    for weekday in range(0, 7):
        visualize.show_apps_sum_revenue(count=count, weekday=weekday, time_range=[9, 23])


if __name__ == '__main__':
    # prepare_data()
    show_best_apps(3)
