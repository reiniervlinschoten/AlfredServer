from src.modules.communicationcentre.messagehandler import handle_message
from src.modules.logging.logger import setup_logger


class Main:
    def __init__(self):
        self.logger = setup_logger(__name__)
        self.mqtt = None
        self.devices = []
        self.database = None

    def setup_mqtt(self, mqtt_object):
        mqtt_object.set_main(self)
        self.mqtt = mqtt_object

    def add_device(self, device_object):
        if device_object not in self.devices:
            device_object.set_main(self)
            self.devices.append(device_object)
            self.logger.info("{0} was added to the devices".format(device_object.name))
        else:
            self.logger.info("{0} was NOT added to the devices, already exists".format(device_object.name))

    def remove_device(self, device_object):
        if device_object in self.devices:
            self.devices.remove(device_object)
            self.database.remove_device(device_object)
            self.logger.info("{0} was removed from the devices".format(device_object.name))
        else:
            self.logger.info("{0} was NOT removed from the devices, not there".format(device_object.name))

    def add_new_device(self, device_object):
        self.add_device(device_object)
        self.database.add_device(device_object)

    def link_database(self, database_object):
        self.database = database_object

    def handle_message(self, topic, message):
        handle_message(topic, message, self)
