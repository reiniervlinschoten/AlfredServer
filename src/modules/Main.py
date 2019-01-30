from src.modules.communicationcentre.messagehandler import handle_message
from src.modules.logging.logger import setup_logger


class Main:
    def __init__(self):
        self.logger = setup_logger(__name__)
        self.mqtt = None
        self.devices = []

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

    def handle_message(self, topic, message):
        handle_message(topic, message, self)
