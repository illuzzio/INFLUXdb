from influxdb import InfluxDBClient
import threading
from time import sleep
from random import randint

class Param(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def get_value(self):
        return self.value

    def get_name(self):
        return self.name

def add_param_in_list(Key, value):
    list_param[Key] = value


def thread_function():
    global points, list_param, client

    client = InfluxDBClient(host='localhost', port=8086)
    client.create_database('Sorce')
    print(client.get_list_database())
    client.switch_database('Sorce')

    list_param = {}

    for param in range(10):
        param = 'num' + str(param)
        if param not in list_param:
            p = Param(param, randint(0, 100))
            list_param[p.get_name()] = p.get_value()
    print(list_param)
    phase = 0

    while True:
        for Key in list_param:
            if Key not in list_param:
                p = Param(Key, randint(0, 100))
                add_param_in_list(p.get_name(), p.get_value())

            s = [{
                "measurement": "sec",
                "tags": {
                    "param": Key,
                    "phase": phase,
                    "topic": br.topic
                },
                "fields": {
                    "value": list_param[Key]
                }
            }]

            list_param[Key] += randint(-2, 2)
            client.write_points(s)
        phase += 2
        sleep(2)

if name == "main":

    x = threading.Thread(target=thread_function)
    x.start()