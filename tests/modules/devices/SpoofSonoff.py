import ast
import paho.mqtt.client as mqtt

from src.modules.logging.logger import setup_logger


class SpoofSonoff:
    def __init__(self, host, username, password):
        self.client = mqtt.Client()
        self.logger = setup_logger(__name__ + host)
        self.setup_client(host, username, password)
        self.main = None

    def start(self):
        self.client.loop_start()

    def stop(self):
        self.client.disconnect()

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
        self.handle_message_spoof(topic, message)

    def handle_message_spoof(self, topic, message):
        if "sonoff" in topic and "cmd" in topic:
            device = topic.replace("cmd", "").replace("/", "")
            return_topic = "/{0}/status".format(device)
            test = message.split(",")
            gpio = test[0].upper()
            pin = test[1]
            switch = test[2]
            log_message = '{0} {1} Set to {2}'.format(gpio, pin, switch)
            return_message = str({'log': log_message,
                                  'plugin': 1,
                                  'pin': int(pin),
                                  'mode': 'output',
                                  'state': int(switch)
                                  })
            self.client.publish(return_topic, return_message)

    def on_connect(self, client, userdata, flags, rc):
        self.logger.info("Connected with result code " + str(rc))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe('#')

    def on_disconnect(self, client, userdata, flags, rc=0):
        self.logger.info("Disconnected with result code " + str(rc))
        self.client.loop_stop()

    # SETTERS
    def set_main(self, main):
        self.main = main


