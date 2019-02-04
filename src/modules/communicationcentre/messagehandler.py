import ast

from src.modules.devices.Sonoff import Sonoff
from src.modules.exceptions.DeviceNotFoundException import DeviceNotFoundException


def handle_message(topic, message, main):
    """Topics for communicating between client and broker follow the following format:
       /category/direction/command/(optional)target
       - Category: a submodule of Alfred, possibilities: devices
       - Direction: in (Client->Broker)/ out (Broker->Client)
       - Command: The chosen action, examples: set, ask, give
       - (optional) Target: When a particular part of a submodule is targeted, example: a certain device

       Topics from Sonoff devices have a different format pre-installed:
       /devicename/command
       - devicename: The device name that has been given when setting up the Sonoff device
       - command: either cmd (to send a message to the device) or status (which is the device response)"""

    # Read the topic into a list, and remove the first empty string
    topic = topic.split("/")[1:]

    # Handle the data from Client -> Broker
    if topic[1] == "in":
        # Handles data sent about devices from Client -> Broker
        if topic[0] == "devices":
            handle_devices(main, message, topic)
        elif topic[0] == "database":
            handle_database(main, message, topic)

    # Handle the data from Sonoff -> Broker
    if "sonoff" in topic[0]:
        if "status" in topic[1]:
            set_device_toggle(main, message, topic)

def handle_database(main, message, topic):
    if topic[2] == "add":
        device = create_device(message)
        main.add_new_device(device)
    elif topic[2] == "remove":
        device = create_device(message)
        main.remove_device(device)

def create_device(message):
    message = ast.literal_eval(message)
    device = None
    if message["brand"] == "sonoff":
        device = Sonoff(name=message["name"], device_type=message["device_type"], location=message["location"],
                        ip=message["ip"], brand="sonoff")
    return device


def handle_devices(main, message, topic):
    # If length of topic is 3, then we are dealing with a general call about devices
    if len(topic) == 3:
        if topic[2] == "ask":
            if message == "devices":
                return_devices(main)

    # If length of topic is 4, then we are dealing with a particular call to a device
    elif len(topic) == 4:
        target_device = find_device(main, topic)

        if topic[2] == "set":
            set_device(message, target_device, topic)

        elif topic[2] == "ask":
            if message == "status?":
                return_device_link_status(main, target_device)

            elif message == "toggle?":
                return_device_toggle(main, target_device)


def set_device_toggle(main, message, topic):
    information = ast.literal_eval(message)
    new_status = information['state']
    for device in main.devices:
        if device.get_name() == topic[0]:
            device.set_status(new_status)
            break


def return_device_toggle(main, target_device):
    if target_device.get_status() == 1:
        return_message = "on"
    elif target_device.get_status() == 0:
        return_message = "off"
    else:
        return_message = "error"
    main.mqtt.send("/devices/out/give/{0}".format(target_device.name), return_message)


def return_device_link_status(main, target_device):
    if target_device.get_linked():
        return_message = "online"
    else:
        return_message = "offline"
    main.mqtt.send("/devices/out/give/{0}".format(target_device.name), return_message)


def set_device(message, target_device, topic):
    if message == "on":
        target_device.turn_on()
    elif message == "off":
        target_device.turn_off()
    else:
        target_device.logger.debug("Combination of topic ({0}) and message ({1}) is not legal for this "
                                   "apparatus".format(topic, message))


def find_device(main, topic):
    # Find the proper device that has been targeted
    target_name = topic[3]
    target_device = None
    for device in main.devices:
        if device.get_name() == target_name:
            target_device = device
            break
        raise DeviceNotFoundException("Device was not found linked in main.")
    return target_device


def return_devices(main):
    new_message = []
    for device in main.devices:
        new_message.append({"name": device.get_name(),
                            "device_type": device.get_type(),
                            "group": device.get_location(),
                            "ip": device.get_ip(),
                            "brand": device.get_brand(),
                            "linked": device.get_linked(),
                            "status": device.get_status(),
                            })
    main.mqtt.send("/devices/out/give", str(new_message))
