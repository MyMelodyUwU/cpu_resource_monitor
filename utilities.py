import json
import paho.mqtt.client as mqtt

CONFIGURATION_FILENAME = "configuration.json"

def save_configuration(configuration):
    with open(CONFIGURATION_FILENAME, "w") as file:
        json.dump(configuration, file, indent=4)

def initialize_mqtt(mqtt_configuration):
    client = mqtt.Client()
    mqtt_configuration["client"] = client
    client.connect(mqtt_configuration["host"])
    if "on_message" in mqtt_configuration:
        client.on_message = mqtt_configuration["on_message"]
    if "topic_subscribe" in mqtt_configuration:
        client.subscribe(mqtt_configuration["topic_subscribe"])
    client.loop_start()  # starts background MQTT thread

def publish_to_mqtt(mqtt_configuration, payload_as_dictionary):
    mqtt_client = mqtt_configuration["client"]
    topic_publish = mqtt_configuration["topic_publish"]
    payload = json.dumps(payload_as_dictionary)
    mqtt_client.publish(topic_publish, payload)
