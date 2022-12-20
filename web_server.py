#!/usr/bin/env python3

import aggregator # References the subscribe script. 

import click 
from flask import Flask, jsonify
import json
import logging
import queue
import unit_tests
from threading import Thread, Lock as ThreadingLock

run_subscribe = True

app = Flask(__name__)

@app.route('/cpu_usage/<host>', methods=['GET'])

def serve_page(host):

    aggregator_object = aggregator.main(host)
    content = aggregator_object
    print(type(content))
    unit_tests.test_serve_page(content)
    #logger.info(content)
    return content

@click.command()
@click.argument("host", default="localhost")
@click.argument("topic", default="cpu_usage/host_1")
@click.argument("sample_period", default=1)

def main(host, topic, sample_period):
    run_sub_thread = Thread(target = run_subscribe)
    run_sub_thread.start() 
    run_sub_thread.join()

if __name__ == '__main__':
#   main()
    app.run(debug=True, host='0.0.0.0')
