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

def publish_to_mqtt(mqtt_configuration, payload_as_dictionary):
    mqtt_client = mqtt_configuration["client"]
    mqtt_topic = mqtt_configuration["topic"]
    payload = json.dumps(payload_as_dictionary)
    mqtt_client.publish(mqtt_topic, payload)
