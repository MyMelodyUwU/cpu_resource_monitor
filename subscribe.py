#!usr/bin/env python3

import paho.mqtt.client as mqtt
import time
import operations
import json

# These variables are global!

list_cpu_input = []
average_temperature = 0

# -------------------------------------------------------

def do_operations(list_cpu_input):
	output = operations.operation_average(list_cpu_input)	
	return output

def main(host):
	config = operations.read()
	client = operations.make_connection()
	client.connect(config["broker"]) 
	print(config["topic"])
	recieve_msg(client, config["topic"], host)
	change_list_to_json(list_cpu_input)
	content = serve_content()
	#sql_functions.save_content(list_cpu_input)
	return content

def recieve_msg(client, topic, host):

	client.loop_start()

	client.subscribe(topic + "/" + host)
	client.on_message=on_message 

	time.sleep(30)
	client.loop_stop()

def on_message(client, userdata, message):
	decoded_message = str(message.payload.decode("utf-8"))
	#print("received message: " ,decoded_message)
	list_cpu_input.append(decoded_message)

def change_list_to_json(list_cpu_input):
	list_cpu_input = json.dumps(list_cpu_input)


def serve_content():
	content = "The current collected CPU Information is " + str(list_cpu_input)
	return content

if __name__ == '__main__':
	main()