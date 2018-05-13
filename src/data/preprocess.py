import dateutil.parser


def append_revenue(apps, link_data, orders):
    apps[0].append('Revenue')

    counter = 0

    for app in apps[1:]:
        try:
            link = link_data[app[3]]
            sess_id = link['SessionID'].lower()
            orders_by_sess_id = orders[sess_id]
            min_delta = None
            best_index = None

            app_time = dateutil.parser.parse(app[1]).replace(tzinfo=None)

            for index, order in enumerate(orders_by_sess_id):
                order_time = dateutil.parser.parse(order['Time'])
                delta = order_time - app_time
                if not min_delta or delta < min_delta:
                    min_delta = delta
                    best_index = index

            revenue = round(float(orders_by_sess_id[best_index]['Revenue']), 2)
            app.append(revenue)
        except:
            apps.remove(app)
            counter += 1
    print('item without revenue', counter)


def append_time_duration(apps, start_time_index=0, end_time_index=1):
    apps[0].append('Time')
    apps[0].append('Duration')

    for app in apps[1:]:
        date_start = dateutil.parser.parse(app[start_time_index])
        date_end = dateutil.parser.parse(app[end_time_index])
        duration = date_end - date_start
        duration_in_minutes = duration.total_seconds() / 60.0
        app.append(str(round(date_start.hour + (date_start.minute / 60.0), 2)))
        app.append(str(round(duration_in_minutes, 2)))

    return apps


def append_time_in_hours(apps, start_time_index=0):
    apps[0].append('Hours')

    for app in apps[1:]:
        date_start = dateutil.parser.parse(app[start_time_index])
        app.append(str(round(date_start.hour, 2)))

    return apps

def append_time_in_days(apps, start_time_index=0):
    apps[0].append('Weekday')

    for app in apps[1:]:
        date_start = dateutil.parser.parse(app[start_time_index])
        app.append(str(date_start.weekday()))

    return apps
