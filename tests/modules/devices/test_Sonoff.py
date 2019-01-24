import random
import time
import pytest

from src.modules.exceptions.DeviceNotLinkedException import DeviceNotLinkedException


class TestSonoff:
    """This class tests the implementation of the Sonoff Object. It does not look at communication with outside
       apparatus."""

    @pytest.fixture(scope="class")
    def data(self, main, mqtt, mqtt_log, linked_sonoff, unlinked_sonoff):
        """Gathers data from fixtures in conftest.py and assembles it for this test suite"""
        # Sonoff and MQTT have to be linked with Main so Sonoff Object can send messages
        main.setup_mqtt(mqtt)
        for sonoff in (linked_sonoff + unlinked_sonoff):
            main.add_device(sonoff)

        # Assembling
        data = {"linked": linked_sonoff, "unlinked": unlinked_sonoff, "log": mqtt_log}
        yield data

    def test_turn_on_linked(self, data):
        for sonoff in data["linked"]:
            # Send message and initialize it's comparison
            message = sonoff.turn_on()
            proper_format = "/{0}/cmd - gpio,12,1".format(sonoff.get_name())

            # Wait so everything can be handled and logged
            time.sleep(0.01)

            # Get last log line
            file = open(data["log"], 'r')
            loglines = list(file)
            last_line = loglines[-1]

            # Assert that the proper message was sent, and that it was logged
            assert message == proper_format
            assert message in last_line

    def test_turn_off_linked(self, data):
        for sonoff in data["linked"]:
            # Send message and initialize it's comparison
            message = sonoff.turn_off()
            proper_format = "/{0}/cmd - gpio,12,0".format(sonoff.get_name())

            # Wait so everything can be handled and logged
            time.sleep(0.01)

            # Get last log line
            file = open(data["log"], 'r')
            loglines = list(file)
            last_line = loglines[-1]

            # Assert that the proper message was sent, and that it was logged
            assert message == proper_format
            assert message in last_line

    def test_switch_linked(self, data):
        for sonoff in data["linked"]:
            # Set base state to random
            old_state = random.getrandbits(1)
            sonoff.status = old_state

            # Send message and initialize it's comparison
            message = sonoff.switch()
            if old_state == 1:
                proper_format = "/{0}/cmd - gpio,12,0".format(sonoff.get_name())
            elif old_state == 0:
                proper_format = "/{0}/cmd - gpio,12,1".format(sonoff.get_name())
            else:
                proper_format = "Something went wrong with setting base state"

            # Wait so everything can be handled and logged
            time.sleep(0.01)

            # Get last log line
            file = open(data["log"], 'r')
            loglines = list(file)
            last_line = loglines[-1]

            # Assert that the proper message was sent, and that it was logged
            assert message == proper_format
            assert message in last_line

    def test_turn_on_unlinked(self, data):
        for sonoff in data["unlinked"]:
            with pytest.raises(DeviceNotLinkedException) as e:
                # Send message and initialize it's comparison
                sonoff.turn_on()
                proper_error_message = "{0} ({1}) at {2} in {3} could not be reached".format(sonoff.getname(),
                                                                                             sonoff.gettype(),
                                                                                             sonoff.getip(),
                                                                                             sonoff.getgroup())

                # Get last log line for sonoff
                sonoff_log = sonoff.logger.handlers[0].baseFilename
                file = open(sonoff_log, 'r')
                loglines = list(file)
                last_line = loglines[-1]

                # When Sonoff is not linked, it should raise a DeviceNotLinkedException with the given error message
                assert proper_error_message in e.value
                assert proper_error_message in last_line

    def test_turn_off_unlinked(self, data):
        for sonoff in data["unlinked"]:
            with pytest.raises(DeviceNotLinkedException) as e:
                # Send message and initialize it's comparison
                sonoff.turn_off()
                proper_error_message = "{0} ({1}) at {2} in {3} could not be reached".format(sonoff.getname(),
                                                                                             sonoff.gettype(),
                                                                                             sonoff.getip(),
                                                                                             sonoff.getgroup())

                # Get last log line for sonoff
                sonoff_log = sonoff.logger.handlers[0].baseFilename
                file = open(sonoff_log, 'r')
                loglines = list(file)
                last_line = loglines[-1]

                # When Sonoff is not linked, it should raise a DeviceNotLinkedException with the given error message
                assert proper_error_message in e.value
                assert proper_error_message in last_line

    def test_switch_unlinked(self, data):
        for sonoff in data["unlinked"]:
            with pytest.raises(DeviceNotLinkedException) as e:
                # Send message and initialize it's comparison
                sonoff.switch()
                proper_error_message = "{0} ({1}) at {2} in {3} could not be reached".format(sonoff.getname(),
                                                                                             sonoff.gettype(),
                                                                                             sonoff.getip(),
                                                                                             sonoff.getgroup())

                # Get last log line for sonoff
                sonoff_log = sonoff.logger.handlers[0].baseFilename
                file = open(sonoff_log, 'r')
                loglines = list(file)
                last_line = loglines[-1]

                # When Sonoff is not linked, it should raise a DeviceNotLinkedException with the given error message
                assert proper_error_message in e.value
                assert proper_error_message in last_line
