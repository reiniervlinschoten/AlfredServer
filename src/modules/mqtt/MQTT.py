import paho.mqtt.client as mqtt

from src.modules.communicationcentre.messagehandler import handle_message
from src.modules.logging.logger import setup_logger


class MQTT:
    def __init__(self, host, username, password):
        self.client = mqtt.Client()
        self.logger = setup_logger(__name__ + host)
        self.setup_client(host, username, password)

    def start(self):
        self.client.loop_forever()

    def setup_client(self, host, username, password):
        self.client.username_pw_set(username, password)
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message
        self.client.connect(host)

    def send(self, topic, message):
        self.client.publish(topic, message)
        return "{0} - {1}".format(topic, message)

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        message = str(msg.payload, "UTF-8")
        self.logger.info("{0} - {1}".format(topic, message))
        handle_message(topic, message)

    def on_connect(self, client, userdata, flags, rc):
        self.logger.info("Connected with result code " + str(rc))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe('#')

    def on_disconnect(self, client, userdata, flags, rc=0):
        self.logger.info("Disconnected with result code " + str(rc))
        self.client.loop_stop()

    # FUNCTIONS FOR TESTING PURPOSES (NON-BLOCKING)
    def testing_start(self):
        self.client.loop_start()

    def testing_stop(self):
        self.client.disconnect()

