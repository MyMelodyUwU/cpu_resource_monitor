#!/usr/bin/env python3

import queue
from threading import Thread
from threading import Lock as ThreadingLock
import logging

from flask import Flask 
from flask import jsonify

import json

run_subscribe = True

USE_LOCK = True

transaction_lock = ThreadingLock()

import aggregator #References the subscribe script. 

app = Flask(__name__)

#logger = logging.getLogger('my_logs')

@app.route('/CPU/<host>', methods=['GET'])

def serve_page(host):

	#transaction_lock.acquire()
	aggregator_object = aggregator.main(host)
	# this function calls the subscibe script. 
	#transaction_lock.release()
	content = aggregator_object
	#logger.info(content)
	return content

"""
def serve_as_table(content):
	html_table = "<table>"
	print("Hello")
	html_table += "<tr><td>{}</td>".format(content["cpu_percent"])
	html_table += "</table>"
	print(html_table)
	return html_table
"""

def main():
	run_sub_thread = Thread(target = run_subscribe)

	run_sub_thread.start() 

	run_sub_thread.join()

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
