# SimpleServerMonitor
SimpleServerMonitor is a cross-platform tool for monitoring server performance counters.
Processor, memory, network and disk information are available as a graphs from now to twenty-four hours ago via your browser.

### Tech
SimpleServerMonitor uses a number of open source projects:
- [ChartJS]
- [CherryPy]
- [SQLite]
- [Materialize]

### Configure
All available configs located at 'config' directory.
Use **http** python file to configure IP and port.

### Installation on Ubuntu
To install SimpleServerMonitor on your server you should:

Install Python.
```sh
apt-get install python3-dev python3-pip python3-setuptools
```
Install all Python requirements.
```sh
pip3 install --upgrade pip && pip3 install -r requirements.txt
```

Clone SimpleServerMonitor from the repository.
```sh
git clone https://github.com/lyftzeigen/SimpleServerMonitor.git && cd SimpleServerMonitor
```

Add SimpleServerMonitor to autostart. The simplest way to do this is using cron.
Open crontab and add path to start script with @reboot policy.
```sh
crontab -e
```
For example
```sh
@reboot /path/to/start.sh
```
Do not forget make scripts executable.
```sh
chmod +x start.sh stop.sh
```
Finally run the start script.
```sh
./start.sh
```

To stop SimpleServerMonitor do the same.
```sh
./stop.sh
```

[ChartJS]: <http://www.chartjs.org/>
[CherryPy]: <http://cherrypy.org/>
[Materialize]: <http://materializecss.com/>
[SQLite]: <https://docs.python.org/2/library/sqlite3.html>