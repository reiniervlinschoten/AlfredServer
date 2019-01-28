import time
import pytest

from src.modules.devices.Sonoff import Sonoff
from tests.modules.data import keys
from tests.modules.devices.SpoofSonoff import SpoofSonoff


class TestMain:
    @pytest.fixture(scope="class")
    def data(self, main, mqtt, mqtt_log, linked_sonoff, unlinked_sonoff):
        spoof_sonoff = SpoofSonoff(host=keys.MQTT_BROKER, username=keys.MQTT_USERNAME, password=keys.MQTT_PASSWORD)
        spoof_sonoff.start()
        spoof_sonoff.set_main(main)

        main.setup_mqtt(mqtt)

        for sonoff in (linked_sonoff + unlinked_sonoff):
            main.add_device(sonoff)

        yield main
        spoof_sonoff.stop()

    def test_add_sonoff(self, data):
        """Tests the adding of devices to Main"""
        assert len(data.devices) == 10

    def test_handle_message_sonoff(self, data):
        """Tests the integration of the Sonoff within Main"""
        # First find the device that we are working with
        for device in data.devices:
            if device.brand == "sonoff" and device.name == "sonoff0":
                test_device = device

        # Send the proper messages and see if the system reacts
        data.mqtt.send("/sonoff0/cmd", "gpio,12,1")
        time.sleep(0.1)
        assert test_device.get_status() == 1
        data.mqtt.send("/sonoff0/cmd", "gpio,12,0")
        time.sleep(0.1)
        assert test_device.get_status() == 0
        data.mqtt.send("/sonoff0/cmd", "gpio,12,1")
        time.sleep(0.1)
        assert test_device.get_status() == 1

    # Fixture helper functions
    def add_device(self, data):
        new_device = Sonoff(name="sonoff0", device_type="light", group="livingroom", ip="111.111.1.0")
        new_device.linked = True
        data.add_device(new_device)


