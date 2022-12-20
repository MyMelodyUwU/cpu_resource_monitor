#!/usr/bin/env python3
#
# To Do
# ~~~~~
# - Clean-up database connection, how ?

from flask import Flask, jsonify

import utilities

app = Flask(__name__)
connection = None

@app.route('/cpu_usage', methods=['GET'])
def serve_page():
    global connection  # TODO: Fix this !
    if not connection:
        connection = utilities.initialize_database()
    cpu_usage = utilities.read_records(connection)
    return cpu_usage

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
