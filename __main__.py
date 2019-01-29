from src.modules.Main import Main
from src.modules.data import keys
from src.modules.mqtt.MQTT import MQTT

if __name__ == "__main__":
    main = Main()
    main.setup_mqtt(MQTT(host=keys.MQTT_BROKER, username=keys.MQTT_USERNAME, password=keys.MQTT_PASSWORD))
    main.mqtt.client.loop_forever()
