from src.modules.logging.logger import setup_logger


class Main:
    def __init__(self):
        self.logger = setup_logger(__name__)
        self.mqtt = None
        self.devices = []

    def setup_mqtt(self, mqtt_object):
        self.mqtt = mqtt_object
        self.mqtt.start()
        self.logger.info("MQTT Listening started")

    def add_device(self, device_object):
        device_object.set_comm_channel(self.mqtt)
        self.devices.append(device_object)
        self.logger.info("{0} was added to the devices".format(device_object.name))

    # Testing functions
    def setup_mqtt_testing(self, mqtt_object):
        self.mqtt = mqtt_object
        self.mqtt.testing_start()
        self.logger.info("MQTT Listening started in test mode")