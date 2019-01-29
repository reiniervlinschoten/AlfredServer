from abc import abstractmethod

from src.modules.logging.logger import setup_logger


class Device:
    """This is the Device superclass, other devices can inherit from this to make sure that basic functionality
       is the same between all Devices."""
    def __init__(self, name, device_type, group, ip, brand):
        self.name = name
        self.device_type = device_type
        self.group = group
        self.ip = ip
        self.brand = brand
        self.main = None
        self.status = None
        self.linked = None
        self.logger = self.setup_logger()
        self.connect()

    def setup_logger(self):
        return setup_logger(self.name)

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def turn_on(self):
        pass

    @abstractmethod
    def turn_off(self):
        pass

    @abstractmethod
    def switch(self):
        pass

    # COMPARATORS
    # TODO

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
        return self.device_type

    def get_group(self):
        return self.group

    def get_ip(self):
        return self.ip

    def get_status(self):
        return self.status

    def get_linked(self):
        return self.linked

    def get_brand(self):
        return self.brand
