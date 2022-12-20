#!/usr/bin/python3
#
# Publish CPU usage to MQTT
#
# To Do
# ~~~~~
# BUG: Should publish "cpu_architecture" as a retained message
#
# - Implement logging
# - Disambigute CLI "host" argument into ...
#   - "mqtt_host", i.e the MQTT server
#   - "host_name", i.e the name of the host being monitored
#     - Construct the MQTT topic using this CLI argument
# - Provide CLI argument to save configuration as a JSON file
# - Provide CLI argument to load configuration from a JSON file
# - Write some unit tests

import click
import os
import platform
import psutil
import time

import unit_tests
import utilities

def initialize(host, topic_publish, sample_period):
    configuration = {
        "mqtt": {"host": host, "topic_publish": topic_publish},
        "sample_period": sample_period,
    }
    utilities.initialize_mqtt(configuration["mqtt"])
    return configuration

def sample_cpu_specs():
    host_name = os.uname()[1]
    cpu_architecture = {
        "count": psutil.cpu_count(logical=False),
        "processor_type": platform.processor(),
        "host_name": host_name
    }
    unit_tests.test_cpu_specs(cpu_architecture)
    return cpu_architecture

def sample_cpu_usage():
    cpu_usage = {
        "busy_percent": psutil.cpu_percent(interval=1, percpu=True),
        "clock_frequency": psutil.cpu_freq(),
        #   "statistics": psutil.cpu_stats(),
        #   "response_time": psutil.cpu_times(),
    }
    return cpu_usage

@click.command()
@click.argument("host", default="localhost")
@click.argument("topic_publish", default="cpu_usage/host_1")
@click.argument("sample_period", default=1)
def main(host, topic_publish, sample_period):
    configuration = initialize(host, topic_publish, sample_period)
#   utilities.save_configuration(configuration)
    cpu_architecture = sample_cpu_specs()
    print(f"cpu_architecture: {cpu_architecture}")
    utilities.publish_to_mqtt(configuration["mqtt"], cpu_architecture)
    while True:
        cpu_usage = sample_cpu_usage()
        print(f"cpu_usage: {cpu_usage}")
        utilities.publish_to_mqtt(configuration["mqtt"], cpu_usage)
        time.sleep(configuration["sample_period"])

if __name__ == "__main__":
    main()
