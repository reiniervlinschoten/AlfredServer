import ast

from src.modules.mqtt.MQTT import MQTT
from tests.modules.data import running_programs


class SpoofSonoff(MQTT):
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

        elif "sonoff" in topic and "status" in topic:
            name = topic.replace("status", "").replace("/", "")
            for device in running_programs.DEVICES:
                if device.get_name() == name:
                    m = ast.literal_eval(message)  # Evaluate dict in string form
                    device.set_status(m["state"])

