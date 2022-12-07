#!/usr/bin/env python3

# This is used to publish information on the topic 

import click
import GPUtil
import json
import numpy as np
import matplotlib.pyplot as plt
import operations
import paho.mqtt.client as mqtt 
import random
import sys
import time

# These are the global variables ->

client = mqtt.Client()

global_broker = ""
global_topic = ""
#host = ""

# These functions are in alphabetical order! It shows the order the computer

@click.command()
@click.option('--broker', default="mqtt.eclipseprojects.io", help='Broker to Connect To [Default is MQTT Eclipse Projects].')
@click.option('--topic', default='JT', help='Topic name')
#@click.option('--host', default='CPU_1', help='Thread name')

# def take_inputs(broker, topic):
#     broker_topic = (broker, topic)
#     return broker_topic

def main(broker, topic):
    #broker, topic = take_inputs()
    config = operations.read()
    #host = config["host"]
    #client.connect(broker)
    client.connect(config["broker"])
    publish_to_mqtt(config)

def publish_to_mqtt(config): 
    while True:
        count = -1
        max_count = 0
        for i in config["host"]:
            count += 1
            set_host = config["host"][count]
            if(count == max_count) :
                count = 0
            cpu_payload = operations.make_payload()
            client.publish(config["topic"] + "/" + set_host, (cpu_payload))
            print(f"Published: {cpu_payload} in {set_host}")
            time.sleep(1) 

if __name__ == "__main__":
    main()
