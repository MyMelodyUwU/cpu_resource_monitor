#!/usr/bin/env python3

import json
import matplotlib.pyplot as plt# Plotting the axis
import numpy as np
import paho.mqtt.client as mqtt
import psutil

config_file = "config.json" #Config info

temp_list = []

def operation_average(values):
	for i in values:
		temp_list.append(int(i))
	return sum(temp_list) / len(temp_list)

def read():
    file = open(config_file, "r")
    config = json.loads(file.read())
    return config

def make_connection():
	client = mqtt.Client()
	return client

def make_payload():
	cpu_info = {
                "cpu_percent" : psutil.cpu_percent(interval=1,percpu=True),
                "cpu_times" : psutil.cpu_times(), 
                #"cpu_count": psutil.cpu_count(logical=False),
                #"cpu_stats": psutil.cpu_stats(),
                "cpu_freq" : psutil.cpu_freq()
            }
	return json.dumps(cpu_info)