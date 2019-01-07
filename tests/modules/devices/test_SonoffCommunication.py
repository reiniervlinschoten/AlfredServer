import random
import time

import pytest

from src.modules.devices.Sonoff import Sonoff
from tests.modules.data import keys
from tests.modules.devices.SpoofSonoff import SpoofSonoff


class TestSonoffCommunication:
    """This class merely tests the Sonoff communication with a spoof sonoff created on the system. This Spoof Sonoff
    merely mimics the return messages that are being sent."""

    @pytest.fixture(scope="module")
    def data(self):
        client = SpoofSonoff(host=keys.MQTT_BROKER, username=keys.MQTT_USERNAME, password=keys.MQTT_PASSWORD)
        log = client.logger.handlers[0].baseFilename
        client.testing_start()

        data = {"linked": [], "log": log}

        for i in range(0, 3):  # Spoof working Sonoff
            sonoff = Sonoff("sonoff{0}".format(i), "light", "livingroom", "111.111.1.{0}".format(i), client)
            sonoff.linked = True
            data["linked"].append(sonoff)

        return data

    def test_turn_on_linked(self, data):
        for sonoff in data["linked"]:
            sonoff.turn_on()
            time.sleep(0.5)  # Wait so the message can be returned and everything can be handled and logged
            file = open(data["log"], 'r')
            loglines = list(file)
            last_line = loglines[-1]  # Gets the last message in the loglines
            proper_message = str({
                "log": "GPIO 12 Set to 1",
                "plugin": 1,
                "pin": 12,
                "mode": "output",
                "state": 1
            })
            proper_format = "/{0}/status - ".format(sonoff.get_name()) + proper_message
            assert proper_format in last_line

    def test_turn_off_linked(self, data):
        for sonoff in data["linked"]:
            sonoff.turn_off()
            time.sleep(0.5)  # Wait so the message can be returned and everything can be handled and logged
            file = open(data["log"], 'r')
            loglines = list(file)
            last_line = loglines[-1]  # Gets the last message in the loglines
            proper_message = str({
                "log": "GPIO 12 Set to 0",
                "plugin": 1,
                "pin": 12,
                "mode": "output",
                "state": 0
            })
            proper_format = "/{0}/status - ".format(sonoff.get_name()) + proper_message
            assert proper_format in last_line

    def test_switch_linked(self, data):
        for sonoff in data["linked"]:
            # Set base state to random
            old_state = random.getrandbits(1)
            sonoff.status = old_state
            sonoff.switch()

            time.sleep(0.5)  # Wait so everything can be handled and logged
            file = open(data["log"], 'r')
            loglines = list(file)
            last_line = loglines[-1]  # Gets the last message in the loglines

            if old_state == 1:
                proper_message = str({
                    "log": "GPIO 12 Set to 0",
                    "plugin": 1,
                    "pin": 12,
                    "mode": "output",
                    "state": 0
                })
            elif old_state == 0:
                proper_message = str({
                    "log": "GPIO 12 Set to 1",
                    "plugin": 1,
                    "pin": 12,
                    "mode": "output",
                    "state": 1
                })

            proper_format = "/{0}/status - ".format(sonoff.get_name()) + proper_message
            assert proper_format in last_line
