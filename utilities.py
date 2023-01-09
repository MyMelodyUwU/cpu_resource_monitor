import json
import paho.mqtt.client as mqtt
import os
import sqlite3

CONFIGURATION_FILENAME = "configuration.json"
DATABASE_FILENAME = "resource_usage.db"


def save_configuration(configuration):
    with open(CONFIGURATION_FILENAME, "w") as file:
        json.dump(configuration, file, indent=4)

def initialize_database(database_filename=DATABASE_FILENAME):
    connection = sqlite3.connect(DATABASE_FILENAME)
    return connection

def create_database_tables(connection):   
    cursor = connection.cursor()                                                
    cursor.execute('''CREATE TABLE cpu_usage (
            value text, 
            timestamp text)''')
    connection.commit()                                                         
    cursor.close()   

def read_records(connection):
    records = []
    cursor = connection.cursor()                                                
    cursor.execute('SELECT * FROM cpu_usage')
    for row in cursor:
        records.append(row)
    cursor.close()   
    return records

def write_record(connection, record):
    cursor = connection.cursor()                                                
    cursor.execute(
        '''INSERT INTO cpu_usage (value) VALUES (?)''', (record,))
    connection.commit()                                                         
    cursor.close()   

def write_time(connection, record):
    cursor = connection.cursor()                                                
    cursor.execute(
        '''INSERT INTO cpu_usage (timestamp) VALUES (?)''', (record,))
    connection.commit()                                                         
    cursor.close()   

def close_database(connection):
    connection.close()

def initialize_mqtt(mqtt_configuration):
    client = mqtt.Client()
    mqtt_configuration["client"] = client
    client.connect(mqtt_configuration["host"])
    if "on_message" in mqtt_configuration:
        client.on_message = mqtt_configuration["on_message"]
    if "topic_subscribe" in mqtt_configuration:
        client.subscribe(mqtt_configuration["topic_subscribe"])
    client.loop_start()  # starts background MQTT thread

def publish_to_mqtt(mqtt_configuration, payload_as_dictionary, retain=False):
    print(retain)
    print("this is retain^")
    mqtt_client = mqtt_configuration["client"]
    topic_publish = mqtt_configuration["topic_publish"]
    payload = json.dumps(payload_as_dictionary)
    mqtt_client.publish(topic_publish, payload, retain)

def reset_database():
#could i make a var for the resource usage script
    print("checking if the resource usage db exists")
    if os.path.exists("resource_usage.db"):
        print("The file exists.")
        os.system("sh remove_db.sh")
    else:
        print("The file does not exist.")

def reset_MQTT_retained():
#could i make a var for the remove retained script
    print("checking if the remove script exists")
    if os.path.exists("remove_retained_mqtt_msgs.sh"):
        print("The file exists.")
        os.system("sh remove_retained_mqtt_msgs.sh localhost")
    else:
        print("The file does not exist.")

