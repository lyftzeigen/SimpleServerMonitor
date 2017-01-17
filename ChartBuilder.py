import json
import datetime
import numpy as np


def find_unit(max_value):
    units = ['Bytes', 'KBytes', 'MBytes', 'GBytes']
    for i, u in enumerate(units):
        if 1 < max_value / pow(1024, i) < 1024:
            return pow(1024, i), u


def build_scatter_data(start, end, data, max_value=1):
    # In seconds
    time_step = 60 * 5
    half_step = time_step / 2

    # Linspace start-stop interval with time step
    space = [(start + datetime.timedelta(seconds=s))
             for s in range(0, int((end - start).total_seconds()) + 1, time_step)]

    # Create for each time point element the array of values by left and right of half step
    arr = {}
    for date in space:
        stamp = date.timestamp()
        keys = np.array(list(data.keys()))
        keys = keys[keys > stamp - half_step]
        keys = keys[keys < stamp + half_step]
        arr[date] = [data[k] for k in keys]
        for k in keys:
            del data[k]

    # Create scatter dictionary with average values
    ret_data = []
    for k in sorted(arr.keys()):
        ret_data.append({'x': k.strftime('%Y-%m-%d %H:%M:%S'),
                         'y': int(np.mean(arr[k])) / max_value if len(arr[k]) > 0 else 0})

    return ret_data


def build_cpu_chart(start, end, data):
    cpu_data = {}
    for d in data:
        time = d[0]
        cpu = d[1]
        cpu_data[int(time.timestamp())] = cpu

    cpu_data = build_scatter_data(start, end, cpu_data)

    # Set chart data and options
    cpu_chart = {
        'datasets': [
            {
                'label': 'Processor, %',
                'data': cpu_data,
                'fill': True,
                'lineTension': 0.3,
                'backgroundColor': "rgba(75,192,192,0.4)",
                'borderColor': "rgba(75,192,192,1)"
            }
        ]
    }
    options = {
        'legend': {
            'display': True
        },
        'scales': {
            'xAxes': [{
                'type': 'time',
                'time': {
                    'unit': 'hour',
                    'min': start.strftime('%Y-%m-%d %H:00:00'),
                    'max': end.strftime('%Y-%m-%d %H:00:00'),
                    'displayFormats': {
                        'minute': 'HH:mm',
                        'hour': 'HH:mm',
                    }
                },
                'ticks': {
                    'fontFamily': 'Roboto',
                    'autoSkip': True,
                    'autoSkipPadding': 10,
                    'maxRotation': 0
                }
            }],
            'yAxes': [{
                'ticks': {
                    'fontFamily': 'Roboto',
                    'min': 0,
                    'max': 100,
                }
            }]
        },
        'elements': {
            'line': {
                'borderWidth': 2,
            },
            'point': {
                'radius': 0,
                'hoverRadius': 0
            }
        },
        'tooltips': {
            'enabled': False
        },
    }

    return json.dumps({'data': cpu_chart,
                       'options': options})


def build_mem_chart(start, end, data):
    # Fetch data
    mem_data = {}
    for d in data:
        time = d[0]
        mem = d[1]
        mem_data[int(time.timestamp())] = mem

    # Build dataset for chart
    mem_data = build_scatter_data(start, end, mem_data)

    # Set chart data and options
    mem_chart = {
        'datasets': [
            {
                'label': 'Memory, %',
                'data': mem_data,
                'fill': True,
                'lineTension': 0.3,
                'backgroundColor': "rgba(192,75,192,0.4)",
                'borderColor': "rgba(192,75,192,1)"
            }
        ]
    }
    options = {
        'legend': {
            'display': True
        },
        'scales': {
            'xAxes': [{
                'type': 'time',
                'time': {
                    'unit': 'hour',
                    'min': start.strftime('%Y-%m-%d %H:00:00'),
                    'max': end.strftime('%Y-%m-%d %H:00:00'),
                    'displayFormats': {
                        'minute': 'HH:mm',
                        'hour': 'HH:mm',
                    }
                },
                'ticks': {
                    'fontFamily': 'Roboto',
                    'autoSkip': True,
                    'autoSkipPadding': 10,
                    'maxRotation': 0
                }
            }],
            'yAxes': [{
                'ticks': {
                    'fontFamily': 'Roboto',
                    'min': 0,
                    'max': 100,
                }
            }]
        },
        'elements': {
            'line': {
                'borderWidth': 2,
            },
            'point': {
                'radius': 0,
                'hoverRadius': 0
            }
        },
        'tooltips': {
            'enabled': False
        },
    }

    return json.dumps({'data': mem_chart,
                       'options': options})


def build_net_chart(start, end, data):
    # Fetch
    recv_data = {}
    send_data = {}
    for d in data:
        time = d[0]
        # Clip less than zero
        recv = d[1] * (d[1] > 0)
        send = d[2] * (d[2] > 0)
        recv_data[int(time.timestamp())] = - recv
        send_data[int(time.timestamp())] = + send

    max_recv = max([abs(recv_data[k]) for k in recv_data])
    max_send = max([abs(send_data[k]) for k in send_data])
    max_net = max(max_recv, max_send)

    unit_factor, unit = find_unit(max_net)

    # Build dataset for chart
    recv_data = build_scatter_data(start, end, recv_data, unit_factor)
    send_data = build_scatter_data(start, end, send_data, unit_factor)

    # Set chart data and options
    net_chart = {
        'datasets': [{
            'label': 'Received, %s' % unit,
            'data': recv_data,
            'fill': True,
            'lineTension': 0.3,
            'backgroundColor': "rgba(95,120,192,0.4)",
            'borderColor': "rgba(95,120,192,1)"
        }, {
            'label': 'Sent, %s' % unit,
            'data': send_data,
            'fill': True,
            'lineTension': 0.5,
            'backgroundColor': "rgba(192,120,95,0.4)",
            'borderColor': "rgba(192,120,95,1)"
        }]
    }
    options = {
        'legend': {
            'display': True
        },
        'scales': {
            'xAxes': [{
                'type': 'time',
                'time': {
                    'unit': 'hour',
                    'min': start.strftime('%Y-%m-%d %H:00:00'),
                    'max': end.strftime('%Y-%m-%d %H:00:00'),
                    'displayFormats': {
                        'minute': 'HH:mm',
                        'hour': 'HH:mm',
                    }
                },
                'ticks': {
                    'fontFamily': 'Roboto',
                    'autoSkip': True,
                    'autoSkipPadding': 10,
                    'maxRotation': 0
                }
            }],
            'yAxes': [{
                'ticks': {
                    'fontFamily': 'Roboto'
                    # 'min': 0,
                    # 'max': 100,
                }
            }]
        },
        'elements': {
            'line': {
                'borderWidth': 2,
            },
            'point': {
                'radius': 0,
                'hoverRadius': 0
            }
        },
        'tooltips': {
            'enabled': False
        },
    }

    return json.dumps({'data': net_chart,
                       'options': options})


def build_hdd_chart(start, end, data):
    # Fetch
    read_data = {}
    write_data = {}
    for d in data:
        time = d[0]
        # Clip less than zero
        read = d[1] * (d[1] > 0)
        write = d[2] * (d[2] > 0)
        read_data[int(time.timestamp())] = + read
        write_data[int(time.timestamp())] = - write

    max_read = max([abs(read_data[k]) for k in read_data])
    max_write = max([abs(write_data[k]) for k in write_data])
    max_hdd = max(max_read, max_write)

    unit_factor, unit = find_unit(max_hdd)

    # Build dataset for chart
    read_data = build_scatter_data(start, end, read_data, unit_factor)
    write_data = build_scatter_data(start, end, write_data, unit_factor)

    # Set chart data and options
    hdd_chart = {
        'datasets': [{
            'label': 'Write, %s' % unit,
            'data': write_data,
            'fill': True,
            'lineTension': 0.3,
            'backgroundColor': "rgba(95,120,192,0.4)",
            'borderColor': "rgba(95,120,192,1)"
        }, {
            'label': 'Read, %s' % unit,
            'data': read_data,
            'fill': True,
            'lineTension': 0.5,
            'backgroundColor': "rgba(192,120,95,0.4)",
            'borderColor': "rgba(192,120,95,1)"
        }]
    }
    options = {
        'legend': {
            'display': True
        },
        'scales': {
            'xAxes': [{
                'type': 'time',
                'time': {
                    'unit': 'hour',
                    'min': start.strftime('%Y-%m-%d %H:00:00'),
                    'max': end.strftime('%Y-%m-%d %H:00:00'),
                    'displayFormats': {
                        'minute': 'HH:mm',
                        'hour': 'HH:mm',
                    }
                },
                'ticks': {
                    'fontFamily': 'Roboto',
                    'autoSkip': True,
                    'autoSkipPadding': 10,
                    'maxRotation': 0
                }
            }],
            'yAxes': [{
                'ticks': {
                    'fontFamily': 'Roboto'
                    # 'min': 0,
                    # 'max': 100,
                }
            }]
        },
        'elements': {
            'line': {
                'borderWidth': 2,
            },
            'point': {
                'radius': 0,
                'hoverRadius': 0
            }
        },
        'tooltips': {
            'enabled': False
        },
    }

    return json.dumps({'data': hdd_chart,
                       'options': options})
