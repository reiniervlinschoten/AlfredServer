import random
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

        # First find the device that we are working with
        for device in main.devices:
            if device.brand == "sonoff" and device.name == "sonoff0":
                test_device = device

        data = {"main": main, "test_device": test_device, "mqtt_log": mqtt_log}

        yield data

        spoof_sonoff.stop()

    def test_add_sonoff(self, data):
        """Tests the adding of devices to Main"""
        main = data["main"]
        assert len(main.devices) == 10

    def test_handle_message_sonoff_on_off(self, data):
        """Tests the integration of the Sonoff within Main"""
        # Unpack data from fixture
        main = data["main"]
        test_device = data["test_device"]

        # Send the proper message (spoofing an Alfred Client) and see if the system reacts
        main.mqtt.send("/devices/in/set/sonoff0", "on")
        time.sleep(0.1)
        assert test_device.get_status() == 1
        main.mqtt.send("/devices/in/set/sonoff0", "off")
        time.sleep(0.1)
        assert test_device.get_status() == 0
        main.mqtt.send("/devices/in/set/sonoff0", "on")
        time.sleep(0.1)
        assert test_device.get_status() == 1

    def test_handle_message_sonoff_ask_status(self, data, linked_sonoff, unlinked_sonoff):
        # Unpack data from fixture
        main = data["main"]

        for i in linked_sonoff:
            # Ask the status for the device
            main.mqtt.send("/devices/in/set/{0}".format(i.name), "status?")

            # Wait so everything can be handled and logged
            time.sleep(0.01)

            # Read the last line from the log file
            file = open(data["mqtt_log"], 'r')
            loglines = list(file)
            last_line = loglines[-1]
            proper_format = "devices/out/give/{0} - online".format(i.name)
            assert proper_format in last_line

        for i in unlinked_sonoff:
            # Ask the status for the device
            main.mqtt.send("/devices/in/set/{0}".format(i.name), "status?")

            # Wait so everything can be handled and logged
            time.sleep(0.01)

            # Read the last line from the log file
            file = open(data["mqtt_log"], 'r')
            loglines = list(file)
            last_line = loglines[-1]
            proper_format = "devices/out/give/{0} - offline".format(i.name)
            assert proper_format in last_line

    def test_handle_message_sonoff_ask_toggle(self, data):
        # Unpack data from fixture
        main = data["main"]
        test_device = data["test_device"]

        for i in range(0, 5):
            # Randomly initialize the message that is being sent to the Sonoff, and parametrize test data.
            command_num = random.getrandbits(1)
            if command_num == 1:
                command = "on"
                proper_format = "/devices/out/give/sonoff0 - on"
            elif command_num == 0:
                command = "off"
                proper_format = "/devices/out/give/sonoff0 - off"
            else:
                command = "Error"
                proper_format = "Something went wrong with setting base state"

            # Set a testable status for the Sonoff
            main.mqtt.send("/devices/in/set/sonoff0", command)

            # Wait so everything can be handled and logged
            time.sleep(0.01)

            # Ask the Sonoff what its toggle status is
            main.mqtt.send("/devices/in/ask/sonoff0", "toggle?")

            # Wait so everything can be handled and logged
            time.sleep(0.01)

            # Read the last line from the log file
            file = open(data["mqtt_log"], 'r')
            loglines = list(file)
            last_line = loglines[-1]

            assert proper_format in last_line
            assert test_device.get_status == command_num




