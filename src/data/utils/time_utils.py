import dateutil.parser


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
