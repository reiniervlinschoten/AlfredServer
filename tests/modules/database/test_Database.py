class TestDatabase:
    def test_setup_database_devices(self, database):
        expected_columns = ["id", "name", "device_type", "location", "ip", "brand"]
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

    def test_devices_add_double(self, database, linked_sonoff, same_sonoff, same_name_sonoff, same_ip_sonoff):
        counter = 0
        for sonoff in linked_sonoff:
            database.add_device(sonoff)
            counter += 1
            assert len(database.get_devices()) == counter
        for sonoff in (same_sonoff + same_name_sonoff + same_ip_sonoff):
            database.add_device(sonoff)
            assert len(database.get_devices()) == counter

