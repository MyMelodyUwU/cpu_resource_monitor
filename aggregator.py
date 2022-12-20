#!/usr/bin/python3

import click
import time

import utilities

list_cpu_input = []

def on_message(client, userdata, message):
    topic = message.topic
    payload = str(message.payload.decode("utf-8"))
    print(f"Received {topic}: {payload}")
    list_cpu_input.append(payload)

def initialize(host, topic_subscribe):
    configuration = {
        "mqtt": {
            "host": host,
            "on_message": on_message,
            "topic_subscribe": topic_subscribe
        }
    }
    utilities.initialize_mqtt(configuration["mqtt"])
    return configuration

@click.command()
@click.argument("host", default="localhost")
@click.argument("topic_subscribe", default="cpu_usage/#")
def main(host, topic_subscribe):
    configuration = initialize(host, topic_subscribe)
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
