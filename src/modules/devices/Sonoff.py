import functools
import bs4
import requests
from requests import RequestException

from src.modules.exceptions.DeviceNotLinkedException import DeviceNotLinkedException
from src.modules.logging.logger import setup_logger


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
            self.logger.debug(error_message)
            raise DeviceNotLinkedException(error_message)

    return decorate


class Sonoff:
    # TODO: Recheck connection once in a while
    """Wrapper Object for Sonoff Device. Can be used to control Sonoff that has been flashed with ESPEASY."""
    def __init__(self, name, device_type, group, ip):
        self.name = name
        self.type = device_type
        self.group = group
        self.ip = ip
        self.main = None
        self.status = None
        self.linked = None
        self.logger = setup_logger(__name__ + name)
        self.connect()

    def connect(self):
        """Tries to find the named Sonoff device at the given ip"""
        try:
            # Try to connect to the Sonoff on the network and checks its name
            link = requests.get('http://{0}'.format(self.ip), timeout=1)
            title = bs4.BeautifulSoup(link.content).title

            # Check whether the given name is the name of the device
            if title != self.name:
                self.logger.debug('Given name: {0} and found name on the ip: {1} do not match. '
                                  'Converting name to found name!'.format(self.name, title))
                self.name = title

            # Set the device to linked and sends a request to initialize its status
            self.linked = True
            self.ask_status()

        # Handles problem when the device is not found on the network
        except RequestException:
            """When the request times out, no Sonoff is at the given ip"""
            self.logger.debug("No Sonoff found at given ip: {0}".format(self.ip))
            self.linked = False

    @_error_decorator
    def turn_on(self):
        self.logger.info("Sending message: Turn on")
        return self.main.mqtt.send("/{0}/cmd".format(self.name), "gpio,12,1")

    @_error_decorator
    def turn_off(self):
        self.logger.info("Sending message: Turn off")
        return self.main.mqtt.send("/{0}/cmd".format(self.name), "gpio,12,0")

    @_error_decorator
    def switch(self):
        if self.status == 0:
            return self.turn_on()
        elif self.status == 1:
            return self.turn_off()

    @_error_decorator
    def ask_status(self):
        self.logger.info("Sending message: Ask status")
        return self.main.mqtt.send("/{0}/cmd".format(self.name), "status,gpio,12")

    # SETTERS
    def set_status(self, status):
        self.status = status

    def set_main(self, main):
        """Adds a main, the object that does all communication between modules.
        Do not call this yourself, it will be handled when a device is added to main"""
        self.main = main

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
