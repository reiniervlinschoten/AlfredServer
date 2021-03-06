import time
import pytest


class TestMQTT:
    @pytest.fixture(scope="class")
    def data(self, mqtt, mqtt_log):
        yield {"client": mqtt, "log": mqtt_log}

    def test_connect(self, data):
        file = open(data["log"], 'r')
        loglines = list(file)
        last_line = loglines[-1]  # Gets the last message in the loglines
        assert "Connected with result code 0" in last_line

    def test_send_message(self, data):
        message = data["client"].send(topic="/testsend", message="testsend")
        assert message == "/testsend - testsend"

    def test_receive_message(self, data):
        message = data["client"].send(topic="/testreceive", message="testreceive")
        time.sleep(0.1)  # Wait so everything can be handled and logged

        file = open(data["log"], 'r')
        loglines = list(file)
        last_line = loglines[-1]  # Gets the last message in the loglines

        assert message == "/testreceive - testreceive"
        assert message in last_line

        file.close()

    def test_receive_multiple_messages(self, data):
        for i in range(0, 50):
            message = data["client"].send(topic="/test{0}".format(str(i)), message="test{0}".format(str(i)))
            assert message == "/test{0} - test{0}".format(str(i))

        time.sleep(1)  # Wait so everything can be handled and logged
        file = open(data["log"], 'r')
        loglines = list(file)[-50:]

        for i in range(0, 50):
            message = "/test{0} - test{1}".format(str(i), str(i))
            assert message in loglines[i]

        file.close()
