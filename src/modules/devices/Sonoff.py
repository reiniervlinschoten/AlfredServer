import functools
import bs4
import requests
from requests import RequestException

from src.modules.devices.Device import Device
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
                                                                                  self.device_type,
                                                                                  self.ip,
                                                                                  self.location)
            self.logger.debug(error_message)
            raise DeviceNotLinkedException(error_message)

    return decorate


class Sonoff(Device):
    # TODO: Recheck connection once in a while
    """Wrapper Object for Sonoff Device. Can be used to control Sonoff that has been flashed with ESPEASY."""

    def connect(self):
        """Tries to find the named Sonoff device at the given ip"""
        try:
            # Try to connect to the Sonoff on the network and checks its name
            link = requests.get('http://{0}'.format(self.ip), timeout=1)
            title = bs4.BeautifulSoup(link.content, features='html.parser').title.strip('<title>').strip('</title>')

            # Check whether the given name is the name of the device
            if self.name not in title:
                self.logger.debug('Given name: {0} and found name on the ip: {1} do not match.'.format(self.name, title))
            else:
                self.logger.info('Names do match')

            # Set the device to linked and sends a request to initialize its status
            self.linked = True
            # TODO: Temporarily commented out, because ask_status needs a main, but main is not linked when Sonoff is
            #  created
            #  self.ask_status()

        # Handles problem when the device is not found on the network
        except RequestException:
            # When the request times out, no Sonoff is at the given ip
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
