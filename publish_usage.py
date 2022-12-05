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
            usage = psutil.cpu_percent()
            #usage = psutil.virtual_memory().percent
            #usage = GPUtil.showUtilization()
            #print(psutil.virtual_memory().percent)
            #cpu_bar = "█" * int(usage)
            print(usage)
            print(f"Published: {int(usage)} in {set_host}")
            #print(f"Published: {cpu_bar}")
            #client.publish(topic + "/" + set_host, {cpu_bar})
            client.publish(topic + "/" + set_host, int(usage))
            time.sleep(1) 

if __name__ == "__main__":
    main()
