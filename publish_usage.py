#!/usr/bin/env python3

# This is used to publish information on the topic 

import paho.mqtt.client as mqtt 
import random
import time
import operations
import numpy as np
import psutil
import GPUtil
import matplotlib.pyplot as plt
import json
import click
import sys

# These are the global variables ->

client = mqtt.Client()

topic = ""
#host = ""

# These functions are in alphabetical order! It shows the order the computer

@click.command()
@click.option('--broker', default="mqtt.eclipseprojects.io", help='Broker to Connect To [Default is MQTT Eclipse Projects].')
@click.option('--topic', default='JT', help='Topic name')
#@click.option('--host', default='CPU_1', help='Thread name')

def take_inputs(broker, topic):
    main()

def main():
    config = operations.read()
    #host = config["host"]
    client.connect(config["broker"])
    publish_to_mqtt(config)

def publish_to_mqtt(config): 
    print(config["topic"])
    print(config["broker"])
    print(config["host"])
    while True:
        count = -1
        max_count = 0
        for i in config["host"]:
            count += 1
            set_host = config["host"][count]
            if(count == max_count) :
                count = 0
            cpu_info = {
                "cpu_percent" : psutil.cpu_percent(interval=1,percpu=True),
                "cpu_times" : psutil.cpu_times(), 
                #"cpu_count": psutil.cpu_count(logical=False),
                #"cpu_stats": psutil.cpu_stats(),
                "cpu_freq" : psutil.cpu_freq()
            }
            payload = json.dumps(cpu_info)
            #client.publish(topic + "/" + set_host, {cpu_bar})
            client.publish(topic + "/" + set_host, (payload))
            print(f"Published: {payload} in {set_host}")
            time.sleep(1) 

if __name__ == "__main__":
    take_inputs()