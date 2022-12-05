#!/usr/bin/env python3

# This is used to publish information on the topic 

import paho.mqtt.client as mqtt 
import random
import time
import operations
import numpy as np

# These are the global variables ->

client = mqtt.Client()

# These functions are in alphabetical order! It shows the order the computer

def main():
    print("Waking up")
    config = operations.read()
    topic = config["topic"]
    #host = config["host"]
    client.connect(config["broker"]) 
    publish_to_mqtt(topic, config)

def publish_to_mqtt(topic, config): 
    while True:
        count = -1
        max_count = 0
        for i in config["host"]:
            count += 1
            set_host = config["host"][count]
            if(count == max_count) :
                count = 0
            usage = random.randint(0, 30) 
            client.publish(topic + "/" + set_host, int(usage))
            print(f"Published: {usage} in {set_host}")
            time.sleep(1)

if __name__ == "__main__":
    main()
