import os
import json
import cherrypy
import datetime
from DataManager import DataManager
from ChartBuilder import build_cpu_chart, build_mem_chart, build_net_chart, build_hdd_chart


class WebInterface(object):
    def __init__(self):
        self.data_manager = DataManager()

    @cherrypy.expose
    def index(self):
        html = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'public/templates/main.html')).read()
        html = html.replace('%os_name%', self.data_manager.get_platform())
        html = html.replace('%cores_count%', self.data_manager.get_cpus())
        html = html.replace('%total_memory%', self.data_manager.get_total_memory())
        html = html.replace('%total_disk%', self.data_manager.get_total_disk_space())
        return html

    @cherrypy.expose
    def performance_cpu(self):
        # Find data for today
        end = datetime.datetime.today()
        start = end - datetime.timedelta(hours=24)
        cpu_data = self.data_manager.get_cpu_data(start, end)
        return build_cpu_chart(start, end, cpu_data)


    @cherrypy.expose
    def performance_mem(self):
        # Find data for today
        end = datetime.datetime.today()
        start = end - datetime.timedelta(hours=24)
        mem_data = self.data_manager.get_mem_data(start, end)
        return build_mem_chart(start, end, mem_data)

    @cherrypy.expose
    def performance_net(self):
        # Find data for today
        end = datetime.datetime.today()
        start = end - datetime.timedelta(hours=24)
        net_data = self.data_manager.get_net_data(start, end)
        return build_net_chart(start, end, net_data)


    @cherrypy.expose
    def performance_hdd(self):
        # Find data for today
        end = datetime.datetime.today()
        start = end - datetime.timedelta(hours=24)
        hdd_data = self.data_manager.get_hdd_data(start, end)
        return build_hdd_chart(start, end, hdd_data)


    @cherrypy.expose
    def default(self, attr='abc'):
        return open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'public/templates/404.html'))
