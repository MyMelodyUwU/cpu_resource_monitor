#!usr/bin/env python3

import click
import json
import paho.mqtt.client as mqtt
import time

# import time
import unit_tests

# import sql_functions


# These variables are global!

list_cpu_input = []
config_file = "config.json"
client = mqtt.Client()
topic = ""
host = ""

def main(host):
	file = open(config_file, "r")
	config = json.loads(file.read())
	host = config["mqtt"]["host"]
	topic = config["mqtt"]["topic"]
	client.connect(host)
	recieve_msg(client,topic, host)
	content_served = list_cpu_input

	return content_served

def on_message(client, userdata, message):
    decoded_message = str(message.payload.decode("utf-8"))
    print("received message: ", decoded_message)
    list_cpu_input.append(decoded_message)

def recieve_msg(client, topic, host):
	client.loop_start()
	client.subscribe(topic)
	client.on_message = on_message
	time.sleep(5)
	client.loop_stop()

if __name__ == "__main__":
    main()
