import os
import cherrypy
from config import http
from WebInterface import WebInterface
from PerformanceCollector import PerformanceCollector

if __name__ == '__main__':
    pc = PerformanceCollector()
    gui = WebInterface()

    script_path = os.path.dirname(os.path.realpath(__file__))

    conf = {
        '/': {
            'tools.staticdir.on': True,
            'tools.staticdir.root': script_path,
            'tools.staticdir.dir': './public'
        },
        '/favicon.ico': {
            'tools.staticfile.on': True,
            'tools.staticfile.filename': os.path.join(script_path, 'public/images/favicon.ico')
        }
    }

    cherrypy.config.update({'server.socket_host': http.host})
    cherrypy.config.update({'server.socket_port': http.port})
    cherrypy.quickstart(gui, '/', conf)
