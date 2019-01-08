import random
import time

import pytest

from src.modules.devices.Sonoff import Sonoff
from src.modules.exceptions.DeviceNotLinkedException import DeviceNotLinkedException
from src.modules.mqtt.MQTT import MQTT
from tests.modules.data import keys


class TestSonoff:
    """This class merely tests the Sonoff object. It looks at if the objects are sending the proper data when asked to.
    It also looks at error handling when the objects are not online. HOWEVER: it does not look at the receiving end
    of the Sonoff, nor can it look at state changing."""

    @pytest.fixture(scope="module")
    def data(self):
        client = MQTT(host=keys.MQTT_BROKER, username=keys.MQTT_USERNAME, password=keys.MQTT_PASSWORD)
        log = client.logger.handlers[0].baseFilename
        client.testing_start()

        data = {"linked": [], "unlinked": [], "log": log}

        for i in range(0, 3):  # Spoof working Sonoff
            sonoff = Sonoff("sonoff{0}".format(i), "light", "livingroom", "111.111.1.{0}".format(i), client)
            sonoff.linked = True
            data["linked"].append(sonoff)

        for i in range(3, 6):  # Create unlinked Sonoff
            sonoff = Sonoff("sonoff{0}".format(i), "light", "livingroom", "111.111.1.{0}".format(i), client)
            data["unlinked"].append(sonoff)

        yield data
        client.testing_stop()

    def test_turn_on_linked(self, data):
        for sonoff in data["linked"]:
            message = sonoff.turn_on()
            time.sleep(0.01)  # Wait so everything can be handled and logged
            file = open(data["log"], 'r')
            loglines = list(file)
            last_line = loglines[-1]  # Gets the last message in the loglines
            proper_format = "/{0}/cmd - gpio,12,1".format(sonoff.get_name())
            assert message == proper_format
            assert message in last_line

    def test_turn_off_linked(self, data):
        for sonoff in data["linked"]:
            message = sonoff.turn_off()
            time.sleep(0.01)  # Wait so everything can be handled and logged
            file = open(data["log"], 'r')
            loglines = list(file)
            last_line = loglines[-1]  # Gets the last message in the loglines
            proper_format = "/{0}/cmd - gpio,12,0".format(sonoff.get_name())
            assert message == proper_format
            assert message in last_line

    def test_switch_linked(self, data):
        for sonoff in data["linked"]:
            # Set base state to random
            old_state = random.getrandbits(1)
            sonoff.status = old_state

            message = sonoff.switch()
            time.sleep(0.01)  # Wait so everything can be handled and logged
            file = open(data["log"], 'r')
            loglines = list(file)
            last_line = loglines[-1]  # Gets the last message in the loglines
            proper_format = "/{0}/cmd - gpio,12,0".format(sonoff.get_name()) if old_state == 1 \
                else "/{0}/cmd - gpio,12,1".format(sonoff.get_name())
            assert message == proper_format
            assert message in last_line

    def test_turn_on_unlinked(self, data):
        for sonoff in data["unlinked"]:
            with pytest.raises(DeviceNotLinkedException) as e:
                sonoff.turn_on()
                proper_error_message = "{0} ({1}) at {2} in {3} could not be reached".format(sonoff.getname(),
                                                                                             sonoff.gettype(),
                                                                                             sonoff.getip(),
                                                                                             sonoff.getgroup())
                assert proper_error_message in e.value

    def test_turn_off_unlinked(self, data):
        for sonoff in data["unlinked"]:
            with pytest.raises(DeviceNotLinkedException) as e:
                sonoff.turn_off()
                proper_error_message = "{0} ({1}) at {2} in {3} could not be reached".format(sonoff.getname(),
                                                                                             sonoff.gettype(),
                                                                                             sonoff.getip(),
                                                                                             sonoff.getgroup())
                assert proper_error_message in e.value

    def test_switch_unlinked(self, data):
        for sonoff in data["unlinked"]:
            with pytest.raises(DeviceNotLinkedException) as e:
                sonoff.switch()
                proper_error_message = "{0} ({1}) at {2} in {3} could not be reached".format(sonoff.getname(),
                                                                                             sonoff.gettype(),
                                                                                             sonoff.getip(),
                                                                                             sonoff.getgroup())
                assert proper_error_message in e.value
