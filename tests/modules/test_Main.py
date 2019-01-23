import time

import pytest

from src.modules.Main import Main
from src.modules.devices.Sonoff import Sonoff
from src.modules.mqtt.MQTT import MQTT
from tests.modules.data import keys
from tests.modules.devices.SpoofSonoff import SpoofSonoff


class TestMain:
    @pytest.fixture(scope="class")
    def data(self):
        data = Main()
        # Setup a SpoofSonoff to return the proper messages
        spoof = SpoofSonoff(host=keys.MQTT_BROKER, username=keys.MQTT_USERNAME, password=keys.MQTT_PASSWORD)
        spoof.start()

        data.setup_mqtt_testing(MQTT(host=keys.MQTT_BROKER, username=keys.MQTT_USERNAME, password=keys.MQTT_PASSWORD))
        self.add_device(data)

        yield data

        data.mqtt.stop()
        spoof.stop()

    def test_mqtt_init(self, data):
        assert data.mqtt

    def test_add_sonoff(self, data):
        assert len(data.devices) == 1
        assert data.devices[0].name == "sonoff0"

    def test_handle_message_sonoff(self, data):
        data.mqtt.send("/sonoff0/cmd", "gpio,12,1")
        time.sleep(0.1)
        assert data.devices[0].get_status() == 1
        data.mqtt.send("/sonoff0/cmd", "gpio,12,0")
        time.sleep(0.1)
        assert data.devices[0].get_status() == 0
        data.mqtt.send("/sonoff0/cmd", "gpio,12,0")
        time.sleep(0.1)
        assert data.devices[0].get_status() == 0

    # Fixture helper functions
    def add_device(self, data):
        new_device = Sonoff(name="sonoff0", device_type="light", group="livingroom", ip="111.111.1.0")
        new_device.linked = True
        data.add_device(new_device)


