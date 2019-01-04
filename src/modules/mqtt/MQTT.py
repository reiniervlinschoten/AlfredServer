import paho.mqtt.client as mqtt

from src.modules.communicationcentre.messagehandler import handle_message
from src.modules.logging.logger import setup_logger


class MQTT:
    def __init__(self, host, username, password):
        self.client = mqtt.Client()
        self.logger = setup_logger(__name__ + host)
        self.setup_client(host, username, password)
        self.client.loop_start()

    def setup_client(self, host, username, password):
        self.client.username_pw_set(username, password)
        self.client.on_connect = self.on_connect
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

