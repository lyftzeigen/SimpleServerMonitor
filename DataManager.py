import psutil
import sqlite3
import platform
import datetime
import threading
import numpy as np


class DataManager:
    def __init__(self):
        self.lock = threading.Lock()
        self.connection = sqlite3.connect('SimpleServerMonitor.db', check_same_thread=False, detect_types=sqlite3.PARSE_DECLTYPES)
        self.cursor = self.connection.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS cpu (time TIMESTAMP, load REAL)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS mem (time TIMESTAMP, load REAL)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS net (time TIMESTAMP, receive INTEGER, send INTEGER)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS hdd (time TIMESTAMP, read INTEGER, write INTEGER)''')
        self.connection.commit()

    def add_cpu_data(self, load):
        self.lock.acquire()
        self.cursor.execute('''INSERT INTO cpu VALUES(?, ?)''', (datetime.datetime.today(), load))
        self.connection.commit()
        self.lock.release()

    def add_mem_data(self, load):
        self.lock.acquire()
        self.cursor.execute('''INSERT INTO mem VALUES(?, ?)''', (datetime.datetime.today(), load))
        self.connection.commit()
        self.lock.release()

    def add_net_data(self, receive, send):
        self.lock.acquire()
        self.cursor.execute('''INSERT INTO net VALUES(?, ?, ?)''', (datetime.datetime.today(), receive, send))
        self.connection.commit()
        self.lock.release()

    def add_hdd_data(self, read, write):
        self.lock.acquire()
        self.cursor.execute('''INSERT INTO hdd VALUES(?, ?, ?)''', (datetime.datetime.today(), read, write))
        self.connection.commit()
        self.lock.release()

    def get_cpu_data(self, start_time, end_time):
        self.cursor.execute('''SELECT time, load FROM cpu WHERE time BETWEEN ? and ? ORDER BY time''', (start_time, end_time))
        return self.cursor.fetchall()

    def get_mem_data(self, start_time, end_time):
        self.cursor.execute('''SELECT * FROM mem WHERE time BETWEEN ? and ? ORDER BY time''', (start_time, end_time))
        return self.cursor.fetchall()

    def get_net_data(self, start_time, end_time):
        self.cursor.execute('''SELECT * FROM net WHERE time BETWEEN ? and ? ORDER BY time''', (start_time, end_time))
        return self.cursor.fetchall()

    def get_hdd_data(self, start_time, end_time):
        self.cursor.execute('''SELECT * FROM hdd WHERE time BETWEEN ? and ? ORDER BY time''', (start_time, end_time))
        return self.cursor.fetchall()

    def get_platform(self):
        return platform.system() + ' ' + platform.release()

    def get_cpus(self):
        return str(psutil.cpu_count())

    def get_total_memory(self):
        return self.prettify_bytes(psutil.virtual_memory().total)

    def get_total_disk_space(self):
        return self.prettify_bytes(psutil.disk_usage('/').total)

    def prettify_bytes(self, in_bytes):
        if in_bytes < 1024 * 1024:
            return str(round(in_bytes / 1024, 1)) + ' KB'

        if in_bytes < 1024 * 1024 * 1024:
            return str(round(in_bytes / 1024 / 1024, 1)) + ' MB'

        if in_bytes < 1024 * 1024 * 1024 * 1024:
            return str(round(in_bytes / 1024 / 1024 / 1024, 1)) + ' GB'

    def build_chart_data(self, start, end, data):
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
                             'y': int(np.mean(arr[k]) if len(arr[k]) > 0 else 0)})

        return ret_data
