#!/usr/bin/python3
# Publish CPU usage to MQTT
#
# To Do
# ~~~~~
# - Implement logging
# - Disambigute CLI "host" argument into ...
#   - "mqtt_host", i.e the MQTT server
#   - "host_name", i.e the name of the host being monitored
#     - Construct the MQTT topic using this CLI argument
#     - [x] Consider using "import os; os.uname()[1]"
# - Provide CLI argument to save configuration as a JSON file
# - Provide CLI argument to load configuration from a JSON file
# - Write some unit tests

import click
import json
import os
import paho.mqtt.client as mqtt
import platform
import psutil
import time

def initialize(host, topic, sample_period):
    configuration = {
        "mqtt": {"host": host, "topic": topic},
        "sample_period": sample_period,
    }
    initialize_mqtt(configuration["mqtt"])
    return configuration

def initialize_mqtt(mqtt_configuration):
    client = mqtt.Client()
    mqtt_configuration["client"] = client
    client.connect(mqtt_configuration["host"])

def sample_cpu_specs():
    os_uname = os.uname()[1]
    cpu_architecture = {
        "count": psutil.cpu_count(logical=False),
        "processor_type": platform.processor(),
        "uname": os_uname
    }

    return cpu_architecture

def sample_cpu_usage():
    cpu_usage = {
        "busy_percent": psutil.cpu_percent(interval=1, percpu=True),
        "clock_frequency": psutil.cpu_freq(),
        #   "statistics": psutil.cpu_stats(),
        #   "response_time": psutil.cpu_times(),
    }
    return cpu_usage


def publish_to_mqtt(mqtt_configuration, dict_input):
    mqtt_client = mqtt_configuration["client"]
    mqtt_topic = mqtt_configuration["topic"]
    payload = json.dumps(dict_input)
    mqtt_client.publish(mqtt_topic, payload)

def save_to_json(configuration):
	with open("config.json", "w") as file:
		json.dump(configuration, file, indent=4)
		print("written")

@click.command()
@click.argument("host", default="localhost")
@click.argument("topic", default="cpu_usage/host_1")
@click.argument("sample_period", default=1)
def main(host, topic, sample_period):
	configuration = initialize(host, topic, sample_period)
	print(configuration)
	save_to_json(configuration)
	cpu_architecture = sample_cpu_specs()
	print(f"cpu_architecture: {cpu_architecture}")
	publish_to_mqtt(configuration["mqtt"], cpu_architecture)
	while True:
		cpu_usage = sample_cpu_usage()
		print(f"cpu_usage: {cpu_usage}")
		publish_to_mqtt(configuration["mqtt"], cpu_usage)
		time.sleep(configuration["sample_period"])

if __name__ == "__main__":
    main()
