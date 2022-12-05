#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import json
import numpy as np
import matplotlib.pyplot as plt# Plotting the axis

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
