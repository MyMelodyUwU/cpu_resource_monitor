#!/usr/bin/env python3

from flask import Flask, jsonify
import json
import logging
import queue
from threading import Thread, Lock as ThreadingLock

import aggregator # References the subscribe script. 

run_subscribe = True

USE_LOCK = True

transaction_lock = ThreadingLock()

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
