import pytest

from src.modules.Main import Main
from tests.modules.data import keys


class TestMain:
    @pytest.fixture(scope="class")
    def data(self):
        data = Main()
        data.setup_mqtt(host=keys.MQTT_BROKER, username=keys.MQTT_USERNAME, password=keys.MQTT_PASSWORD)
        self.add_device(data)

        data.mqtt.testing_start()
        yield data
        data.mqtt.testing_stop()

    def test_mqtt_init(self, data):
        assert data.mqtt

    def test_handle_message_sonoff(self, data):
        # TODO
        pass

    # Fixture helper functions
    def add_device(self, data):
        data.add_device(type="sonoff", information={"name": "sonoff0",
                                                    "device_type": "light",
                                                    "group": "livingroom",
                                                    "ip": "111.111.1.0",
                                                    "comm_channel": data.mqtt})
        data.devices["sonoff0"].linked = True  # Fake working sonoff
