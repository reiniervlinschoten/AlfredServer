from src.modules.data import keys
from src.modules.mqtt.MQTT import MQTT

if __name__ == "__main__":
    listener = MQTT(keys.MQTT_BROKER, keys.MQTT_USERNAME, keys.MQTT_PASSWORD)
    listener.start()
