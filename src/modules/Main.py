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
        self.mqtt.start()
        self.logger.info("MQTT Listening started")

    def add_device(self, device_object):
        device_object.set_main(self)
        self.devices.append(device_object)
        self.logger.info("{0} was added to the devices".format(device_object.name))

    def handle_message(self, topic, message):
        handle_message(topic, message, self)

    # Testing functions
    def setup_mqtt_testing(self, mqtt_object):
        self.mqtt = mqtt_object
        self.mqtt.start()
        self.logger.info("MQTT Listening started in test mode")