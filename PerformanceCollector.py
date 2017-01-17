import time
import psutil
import datetime
import threading
from DataManager import DataManager


class PerformanceCollector:
    def __init__(self):
        self.dump_interval = 60  # Seconds
        self.data_manager = DataManager()
        self.cpu_thread = threading.Thread(target=self.collect_cpu_performance)
        self.memory_thread = threading.Thread(target=self.collect_mem_performance)
        self.network_thread = threading.Thread(target=self.collect_net_performance)
        self.disk_thread = threading.Thread(target=self.collect_hdd_performance)

        print('[', datetime.datetime.today(), ']', 'Start')
        self.cpu_thread.start()
        self.memory_thread.start()
        self.network_thread.start()
        self.disk_thread.start()

    def collect_cpu_performance(self):
        while True:
            cpu = psutil.cpu_percent(self.dump_interval)
            self.data_manager.add_cpu_data(cpu)

    def collect_mem_performance(self):
        while True:
            time.sleep(self.dump_interval)
            mem = psutil.virtual_memory().percent
            self.data_manager.add_mem_data(mem)

    def collect_net_performance(self):
        while True:
            net = psutil.net_io_counters()
            sent_old = net.bytes_sent
            receive_old = net.bytes_recv
            time.sleep(self.dump_interval)
            net = psutil.net_io_counters()
            sent = net.bytes_sent
            receive = net.bytes_recv
            self.data_manager.add_net_data(receive - receive_old, sent - sent_old)

    def collect_hdd_performance(self):
        while True:
            disk = psutil.disk_io_counters()
            read_old = disk.read_bytes
            write_old = disk.write_bytes
            time.sleep(self.dump_interval)
            disk = psutil.disk_io_counters()
            read = disk.read_bytes
            write = disk.write_bytes
            self.data_manager.add_hdd_data(read - read_old, write - write_old)

    def wait(self):
        self.cpu_thread.join()
        self.memory_thread.join()
        self.network_thread.join()
        self.disk_thread.join()
