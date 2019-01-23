import ast


def handle_message(topic, message, main):
    topic = topic.split("/")
    if "sonoff" in topic[0]:
        if "status" in topic[1]:
            information = ast.literal_eval(message)
            new_status = information['state']
            for device in main.devices:
                if device.get_name() == topic[0]:
                    device.set_status(new_status)
                    break
