#!/usr/bin/python3
#
# Usage
# ~~~~~
# python ./monitor.py
# python ./aggregator.py
#
# sqlite3 resource_usage.db
# sqlite> .help
# sqlite> .tables
# sqlite> select * from cpu_usage;
# sqlite> .quit

import click
import json
import queue

import utilities

connection = None  # TODO: Fix this !
resource_queue = queue.Queue()

def on_message(client, userdata, message):
    topic = message.topic
    payload = str(message.payload.decode("utf-8"))
    print(f"Received {topic}: {payload}")
    cpu_usage = json.loads(payload)
    busy_percent = cpu_usage["busy_percent"]
    busy_total = sum(busy_percent)
    resource_queue.put(busy_total)

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
    global connection  # TODO: Fix this !
    configuration = initialize(host, topic_subscribe)
    connection = utilities.initialize_database()
#   utilities.create_database_tables(connection)  # once only
    try:
        while True:
            busy_total = resource_queue.get()
            utilities.write_record(connection, busy_total)
            print(f"Database write: {busy_total}")
    except KeyboardInterrupt:
        utilities.close_database(connection)
        print("Database closed")

if __name__ == "__main__":
    main()
