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

    def test_add_devices(self, database, linked_sonoff):
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

    def test_search_device(self, database, linked_sonoff):
        for sonoff in linked_sonoff:
            database.add_device(sonoff)
        for sonoff in linked_sonoff:
            assert database.search_device_name(sonoff)

    def test_device_remove(self, database, linked_sonoff):
        for sonoff in linked_sonoff:
            database.add_device(sonoff)
            assert database.search_device_name(sonoff)

        assert len(database.get_devices()) == 5

        test_device = None
        for device in linked_sonoff:
            if device.brand == "sonoff" and device.name == "sonoff0":
                test_device = device
                break

        database.remove_device(test_device)
        assert len(database.get_devices()) == 4
        assert not database.search_device_name(test_device)

    def test_device_remove_double(self, database, linked_sonoff):
        for sonoff in linked_sonoff:
            database.add_device(sonoff)

        assert len(database.get_devices()) == 5

        test_device = None
        for device in linked_sonoff:
            if device.brand == "sonoff" and device.name == "sonoff0":
                test_device = device
                break

        database.remove_device(test_device)
        assert len(database.get_devices()) == 4
        assert not database.search_device_name(test_device)

        database.remove_device(test_device)
        assert len(database.get_devices()) == 4
        assert not database.search_device_name(test_device)
