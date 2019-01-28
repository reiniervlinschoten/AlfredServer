import ast


def handle_message(topic, message, main):
    # Read the topic into a list, and remove the first empty string
    topic = topic.split("/")[1:]

    # Handle the data from Client -> Broker
    if topic[1] == "in":
        # Handles data sent about devices from Client -> Broker
        if topic[0] == "devices":
            # Find the proper device that has been targeted
            target_name = topic[3]
            for device in main.devices:
                if device.get_name() == target_name:
                    target_device = device
                    break

            if topic[2] == "set":
                if message == "on":
                    target_device.turn_on()
                elif message == "off":
                    target_device.turn_off()
                else:
                    target_device.logger.debug("Combination of topic ({0}) and message ({1}) is not legal for this "
                                               "apparatus".format(topic, message))

            elif topic[2] == "ask":
                if message == "status?":
                    if target_device.get_linked():
                        return_message = "online"
                    else:
                        return_message = "offline"
                    main.mqtt.send("/devices/out/give/{0}".format(target_device.name), return_message)

                elif message == "toggle?":
                    if target_device.get_status() == 1:
                        return_message = "on"
                    elif target_device.get_status() == 0:
                        return_message = "off"
                    else:
                        return_message = "error"
                    main.mqtt.send("/devices/out/give/{0}".format(target_device.name), return_message)

    # Handle the data from Sonoff -> Broker
    if "sonoff" in topic[0]:
        if "status" in topic[1]:
            information = ast.literal_eval(message)
            new_status = information['state']
            for device in main.devices:
                if device.get_name() == topic[0]:
                    device.set_status(new_status)
                    break
