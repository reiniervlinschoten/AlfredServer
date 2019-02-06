import time

import pytest


class TestMainDatabase:
    # TODO: See if this can be sped up (problem: both MQTT and Database calls, asyncio?)
    @pytest.fixture(scope="function")
    def database_main(self, mqtt, database, main):
        main.setup_mqtt(mqtt)
        main.link_database(database)
        yield main

    def test_add_device(self, database_main, linked_sonoff):
        counter = 0
        for sonoff in linked_sonoff:
            sonoff_dict = sonoff.__dict__

            # Remove unnecessary information
            sonoff_dict.pop('main', None)
            sonoff_dict.pop('logger', None)
            sonoff_dict.pop('status', None)
            sonoff_dict.pop('linked', None)

            database_main.mqtt.send("/database/in/add/device", str(sonoff_dict))
            time.sleep(2)
            counter += 1

            assert len(database_main.database.get_devices()) == counter
            assert database_main.database.search_device(sonoff)

    def test_add_device_twice(self, database_main, linked_sonoff):
        counter = 0
        for sonoff in linked_sonoff:
            sonoff_dict = sonoff.__dict__

            # Remove unnecessary information
            sonoff_dict.pop('main', None)
            sonoff_dict.pop('logger', None)
            sonoff_dict.pop('status', None)
            sonoff_dict.pop('linked', None)

            database_main.mqtt.send("/database/in/add/device", str(sonoff_dict))
            time.sleep(2)
            database_main.mqtt.send("/database/in/add/device", str(sonoff_dict))
            time.sleep(2)
            counter += 1
            time.sleep(2)

            assert len(database_main.database.get_devices()) == counter
            assert database_main.database.search_device(sonoff)

    def test_remove_device(self, database_main, linked_sonoff):
        counter = 0
        # Add devices
        for sonoff in linked_sonoff:
            sonoff_dict = sonoff.__dict__

            # Remove unnecessary information
            sonoff_dict.pop('main', None)
            sonoff_dict.pop('logger', None)
            sonoff_dict.pop('status', None)
            sonoff_dict.pop('linked', None)

            database_main.mqtt.send("/database/in/add/device", str(sonoff_dict))
            time.sleep(2)
            counter += 1

            assert len(database_main.database.get_devices()) == counter
            assert database_main.database.search_device(sonoff)

        # Remove devices
        for sonoff in linked_sonoff:
            sonoff_dict = sonoff.__dict__

            # Remove unnecessary information
            sonoff_dict.pop('main', None)
            sonoff_dict.pop('logger', None)
            sonoff_dict.pop('status', None)
            sonoff_dict.pop('linked', None)

            database_main.mqtt.send("/database/in/remove/device", str(sonoff_dict))
            counter -= 1
            time.sleep(2)

            assert len(database_main.database.get_devices()) == counter
            assert not database_main.database.search_device(sonoff)

    def test_remove_device_double(self, database_main, linked_sonoff):
        counter = 0
        # Add devices
        for sonoff in linked_sonoff:
            sonoff_dict = sonoff.__dict__

            # Remove unnecessary information
            sonoff_dict.pop('main', None)
            sonoff_dict.pop('logger', None)
            sonoff_dict.pop('status', None)
            sonoff_dict.pop('linked', None)

            database_main.mqtt.send("/database/in/add/device", str(sonoff_dict))
            counter += 1
            time.sleep(2)

            assert len(database_main.database.get_devices()) == counter
            assert database_main.database.search_device(sonoff)

        # Remove devices twice
        for sonoff in linked_sonoff:
            sonoff_dict = sonoff.__dict__

            # Remove unnecessary information
            sonoff_dict.pop('main', None)
            sonoff_dict.pop('logger', None)
            sonoff_dict.pop('status', None)
            sonoff_dict.pop('linked', None)

            database_main.mqtt.send("/database/in/remove/device", str(sonoff_dict))
            database_main.mqtt.send("/database/in/remove/device", str(sonoff_dict))
            counter -= 1
            time.sleep(2)

            assert len(database_main.database.get_devices()) == counter
            assert not database_main.database.search_device(sonoff)

            assert len(database_main.database.get_devices()) == counter
            assert not database_main.database.search_device(sonoff)

    def test_populate_devices(self, database_main, linked_sonoff):
        assert len(database_main.devices) == 0
        for device in linked_sonoff:
            database_main.database.add_device(device)
        database_main.populate_devices()
        assert len(database_main.database.get_devices()) == len(linked_sonoff)
