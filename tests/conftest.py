import pytest

from src.modules.mqtt.MQTT import MQTT
from tests.modules.data import keys


@pytest.fixture(scope="session")
def mqtt():
    mqtt = MQTT(host=keys.MQTT_BROKER, username=keys.MQTT_USERNAME, password=keys.MQTT_PASSWORD)
    mqtt.testing_start()
    yield mqtt
    mqtt.testing_stop()


@pytest.fixture(scope="session")
def linked_sonoff():
    pass


@pytest.fixture(scope="session")
def unlinked_sonoff():
    pass


@pytest.fixture(scope="session")
def spoof_sonoff():
    pass


@pytest.fixture(scope="session")
def main():
    pass










