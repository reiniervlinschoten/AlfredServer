from src.modules.data import keys, running_programs
from src.modules.mqtt.MQTT import MQTT

if __name__ == "__main__":
    running_programs.MQTT_CLIENT = MQTT(keys.MQTT_BROKER, keys.MQTT_USERNAME, keys.MQTT_PASSWORD)
    running_programs.MQTT_CLIENT.start()
