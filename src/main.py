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
    file_utils.write(apps)
    file_utils.write_files_by_app_name(apps)
    print('finished data preprocessing!')


def show_graphs():
    visualize.show_apps_by_property('Duration', 1)
    visualize.show_apps_by_property('Revenue', 1)
    visualize.show_apps_by_property('Duration', 1 / 50)
    visualize.show_apps_by_property('Revenue', 1 / 50)
    visualize.show_apps_difference_by_properties('Revenue', 'Duration', 1)
    visualize.show_apps_max_revenue()


def show_best_apps(count):
    pass


if __name__ == '__main__':
    prepare_data()
    show_graphs()
    show_best_apps(3)
