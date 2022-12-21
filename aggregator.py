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
import time
import utilities

connection = None  # TODO: Fix this !
resource_queue = queue.Queue()
no_of_cpus = 4

def on_message(client, userdata, message):
    topic = message.topic
    payload = str(message.payload.decode("utf-8"))
    print(f"Received {topic}: {payload}")
    cpu_usage = json.loads(payload)
    cpu_arch = json.load(payload)
    cpu_count = cpu_arch["count"]
    busy_percent = cpu_usage["busy_percent"]
    busy_total = sum(busy_percent)
    resource_queue.put(busy_total)

def generate_current_time():
	unix_time = time.time()
	utilities.write_time(connection, unix_time)
	print("Time written into db: {unix_time}")

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
    #utilities.create_database_tables(connection)  # once only
    utilities.write_record(connection, payload)
    try:
        while True:
            busy_total = (resource_queue.get() / no_of_cpus)
            generate_current_time()
            utilities.write_record(connection, busy_total)
            print(f"Database write: {busy_total}")
    except KeyboardInterrupt:
        utilities.close_database(connection)
        print("Database closed")

if __name__ == "__main__":
    main()
