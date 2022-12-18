#!usr/bin/env python3

import json
#import operations
import paho.mqtt.client as mqtt
import time
import unit_tests
#import sql_functions

# These variables are global!

list_cpu_input = []

# -------------------------------------------------------

def do_operations(list_cpu_input):
	output = operations.operation_average(list_cpu_input)	
	return output

def main(host):
	config = operations.read()
	client = operations.make_connection()
	client.connect(config["broker"]) 
	recieve_msg(client, config["topic"], host)
	#unit_tests.check_cpu(list_cpu_input)
	content_served = list_cpu_input
	#sql_functions.save_content(list_cpu_input)
	return content_served

def on_message(client, userdata, message):
	decoded_message = str(message.payload.decode("utf-8"))
	#print("received message: " ,decoded_message)
	list_cpu_input.append(decoded_message)

def recieve_msg(client, topic, host):

	client.loop_start()

	client.subscribe(topic + "/" + host)
	client.on_message=on_message 

	time.sleep(5)
	client.loop_stop()

if __name__ == '__main__':
	main()
