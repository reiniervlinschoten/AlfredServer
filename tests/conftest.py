import os

import pytest

from src.modules.Main import Main
from src.modules.database.Database import Database
from src.modules.devices.Sonoff import Sonoff
from src.modules.mqtt.MQTT import MQTT
from tests.modules.data import keys


@pytest.fixture(scope="class")
def mqtt():
    mqtt = MQTT(host=keys.MQTT_BROKER, username=keys.MQTT_USERNAME, password=keys.MQTT_PASSWORD)
    mqtt.start()
    yield mqtt
    mqtt.stop()


@pytest.fixture(scope="class")
def mqtt_log(mqtt):
    log = mqtt.logger.handlers[0].baseFilename
    yield log


@pytest.fixture(scope="session")
def linked_sonoff():
    linked_sonoff = []
    for i in range(0, 5):  # Spoof working Sonoff
        sonoff = Sonoff(name="sonoff{0}".format(i),
                        device_type="light",
                        location="livingroom",
                        ip="111.111.1.{0}".format(i),
                        brand="sonoff")
        sonoff.linked = True
        linked_sonoff.append(sonoff)
    yield linked_sonoff


@pytest.fixture(scope="session")
def unlinked_sonoff():
    unlinked_sonoff = []
    for i in range(5, 10):  # Spoof working Sonoff
        sonoff = Sonoff(name="sonoff{0}".format(i),
                        device_type="light",
                        location="livingroom",
                        ip="111.111.1.{0}".format(i),
                        brand="sonoff")
        unlinked_sonoff.append(sonoff)
    yield unlinked_sonoff


@pytest.fixture(scope="session")
def same_sonoff():
    same_sonoff = []
    for i in range(0, 5):
        sonoff = Sonoff(name="sonoff{0}".format(i),
                        device_type="light",
                        location="livingroom",
                        ip="111.111.1.{0}".format(i),
                        brand="sonoff")
        same_sonoff.append(sonoff)
    yield same_sonoff


@pytest.fixture(scope="session")
def same_name_sonoff():
    same_name_sonoff = []
    for i in range(0, 5):
        sonoff = Sonoff(name="sonoff{0}".format(i),
                        device_type="light",
                        location="livingroom",
                        ip="111.111.1.{0}".format(i + 10),
                        brand="sonoff")
        same_name_sonoff.append(sonoff)
    yield same_name_sonoff


@pytest.fixture(scope="session")
def same_ip_sonoff():
    same_ip_sonoff = []
    for i in range(0, 5):
        sonoff = Sonoff(name="sonoff{0}".format(i + 10),
                        device_type="light",
                        location="livingroom",
                        ip="111.111.1.{0}".format(i),
                        brand="sonoff")
        same_ip_sonoff.append(sonoff)
    yield same_ip_sonoff


@pytest.fixture(scope="function")
def database():
    if os.path.exists("tests"):
        test_db_path = "tests/modules/database/test_database.db"
    else:
        test_db_path = "test_database.db"
    database = Database(test_db_path)
    yield database
    os.remove(test_db_path)  # Remove testing database


@pytest.fixture(scope="class")
def main():
    main = Main()
    yield main
