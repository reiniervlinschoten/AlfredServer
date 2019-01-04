import pytest

from src.modules.exceptions.DeviceNotLinkedException import DeviceNotLinkedException


class TestSonoff:

    def test_turn_on_linked(self, dict_of_sonoff):
        for sonoff in dict_of_sonoff["linked"]:
            sonoff.turnon()
            assert sonoff.status() == 1

    def test_turn_off_linked(self, dict_of_sonoff):
        for sonoff in dict_of_sonoff["linked"]:
            sonoff.turnoff()
            assert sonoff.status() == 0

    def test_switch_linked(self, dict_of_sonoff):
        for sonoff in dict_of_sonoff["linked"]:
            old_status = sonoff.status()
            sonoff.switch()
            new_status = sonoff.status()
            assert abs(new_status - old_status) == 1  # Switching will make a 1 difference either way

    def test_turn_on_unlinked(self, dict_of_sonoff):
        for sonoff in dict_of_sonoff["unlinked"]:
            with pytest.raises(DeviceNotLinkedException) as e:
                sonoff.turnon()
                proper_error_message = "{0} ({1}) at {2} in {3} could not be reached".format(sonoff.getname(),
                                                                                             sonoff.gettype(),
                                                                                             sonoff.getip(),
                                                                                             sonoff.getgroup())
                assert proper_error_message in e.value

    def test_turn_off_unlinked(self, dict_of_sonoff):
        for sonoff in dict_of_sonoff["unlinked"]:
            with pytest.raises(DeviceNotLinkedException) as e:
                sonoff.turnoff()
                proper_error_message = "{0} ({1}) at {2} in {3} could not be reached".format(sonoff.getname(),
                                                                                             sonoff.gettype(),
                                                                                             sonoff.getip(),
                                                                                             sonoff.getgroup())
                assert proper_error_message in e.value

    def test_switch_unlinked(self, dict_of_sonoff):
        for sonoff in dict_of_sonoff["unlinked"]:
            with pytest.raises(DeviceNotLinkedException) as e:
                sonoff.switch()
                proper_error_message = "{0} ({1}) at {2} in {3} could not be reached".format(sonoff.getname(),
                                                                                             sonoff.gettype(),
                                                                                             sonoff.getip(),
                                                                                             sonoff.getgroup())
                assert proper_error_message in e.value
