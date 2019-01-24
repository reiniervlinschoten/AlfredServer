import random
import time

import pytest


class TestSonoffCommunication:
    """This class merely tests the Sonoff communication with a spoof sonoff created on the system. This Spoof Sonoff
    merely mimics the return messages that are being sent."""

    @pytest.fixture(scope="class")
    def data(self, mqtt, mqtt_log, main, linked_sonoff, spoof_sonoff):
        main.setup_mqtt(mqtt)
        spoof_sonoff.set_main(main)
        for sonoff in linked_sonoff:
            main.add_device(sonoff)

        data = {"linked": linked_sonoff, "log": mqtt_log}
        yield data

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
            assert sonoff.get_status() == 1

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
            assert sonoff.get_status() == 0

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
                proper_status = 0

            elif old_state == 0:
                proper_message = str({
                    "log": "GPIO 12 Set to 1",
                    "plugin": 1,
                    "pin": 12,
                    "mode": "output",
                    "state": 1
                })
                proper_status = 1

            proper_format = "/{0}/status - ".format(sonoff.get_name()) + proper_message
            assert proper_format in last_line
            assert sonoff.get_status() == proper_status
