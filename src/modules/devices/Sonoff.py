import functools

import bs4
import requests
from requests import RequestException

from src.modules.data import running_programs
from src.modules.exceptions.DeviceNotLinkedException import DeviceNotLinkedException


# DECORATORS
def _error_decorator(func):
    @functools.wraps(func)
    def decorate(*args, **kwargs):
        self = args[0]
        if self.linked:
            return func(*args, **kwargs)
        else:
            error_message = "{0} ({1}) at {2} in {3} could not be reached".format(self.name,
                                                                                  self.type,
                                                                                  self.ip,
                                                                                  self.group)
            raise DeviceNotLinkedException(error_message)

    return decorate


class Sonoff:
    def __init__(self, name, type, group, ip, comm_channel=running_programs.MQTT_CLIENT):
        self.name = name
        self.type = type
        self.group = group
        self.ip = ip
        self.comm_channel = comm_channel
        self.status = None
        self.linked = False
        self.connect()

    def connect(self):
        """Tries to find the named Sonoff device at the given ip"""
        try:
            link = requests.get('http://{0}'.format(self.ip), timeout=1)
            title = bs4.BeautifulSoup(link.content).title
            if title != self.name:
                """Handles typos in name"""
                print('Given name: {0} and found name on the ip: {1} do not match. '
                      'Converting name to found name!'.format(self.name, title))
                self.name = title
            self.linked = True
            self.ask_status()
        except RequestException:
            """When the request times out, no Sonoff is at the given ip"""
            print("No device was found on given ip: {0}".format(self.ip))

    @_error_decorator
    def turn_on(self):
        return self.comm_channel.send("/{0}/cmd".format(self.name), "gpio,12,1")

    @_error_decorator
    def turn_off(self):
        return self.comm_channel.send("/{0}/cmd".format(self.name), "gpio,12,0")

    @_error_decorator
    def switch(self):
        if self.status == 0:
            return self.turn_on()
        elif self.status == 1:
            return self.turn_off()

    @_error_decorator
    def ask_status(self):
        return self.comm_channel.send("/{0}/cmd".format(self.name), "status,gpio,12")

    # GETTERS
    def get_name(self):
        return self.name

    def get_type(self):
        return self.type

    def get_group(self):
        return self.group

    def get_ip(self):
        return self.ip

    def get_status(self):
        return self.status

    def get_linked(self):
        return self.linked
