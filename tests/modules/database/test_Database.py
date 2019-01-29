import os

import pytest

from src.modules.database.Database import Database
from src.modules.devices.Sonoff import Sonoff


class TestDatabase:
    @pytest.fixture(scope="function")
    def database(self):
        if os.path.exists("tests"):
            test_db_path = "tests/modules/database/test_database.db"
        else:
            test_db_path = "test_database.db"
        database = Database(test_db_path)
        yield database
        os.remove(test_db_path)  # Remove testing database

    def test_setup_database_devices(self, database):
        expected_columns = ["id", "name", "device_type", "group", "ip", "brand"]
        table_exists_query = "SELECT count(*) FROM sqlite_master WHERE type='table' AND name='devices';"
        list_columns_query = "SELECT * FROM 'devices'"

        table_exists = database.query(table_exists_query)
        assert table_exists[0][0] == 1

        columns = database.query(list_columns_query, return_val="description")
        list_columns = [column[0] for column in columns]
        assert list_columns == expected_columns

    def test_devices(self, database, linked_sonoff):
        counter = 0
        for sonoff in linked_sonoff:
            database.add_device(sonoff)
            counter += 1
            assert len(database.get_devices()) == counter

    def test_devices_add_double(self, database, linked_sonoff):
        counter = 0
        for sonoff in linked_sonoff:
            database.add_device(sonoff)
            counter += 1
            assert len(database.get_devices()) == counter
        for sonoff in linked_sonoff:
            database.add_device(sonoff)
            assert len(database.get_devices()) == counter

