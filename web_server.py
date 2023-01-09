#!/usr/bin/env python3
#
# To Do
# ~~~~~
# - Clean-up database connection, how ?

from flask import Flask, jsonify, render_template
import sqlite3
import utilities
import os

app = Flask(__name__)
connection = None

@app.route('/cpu_usage', methods=['GET'])
def serve_page():
    global connection  
    sqlite3.connect('resource_usage.db') 
    if not connection:
        connection = utilities.initialize_database()
    #cpu_usage = utilities.read_records(connection)
    cursor = connection.cursor()
    #cursor.execute('SELECT * FROM cpu_usage')
    cursor.execute('PRAGMA table_info(fred)') # find table info
    #cpu_usage = cursor.execute('SELECT AVG(value) FROM cpu_usage')
    cpu_usage = cursor.fetchall()
    print(cpu_usage)
    column_names = [row[1] for row in cpu_usage]
    print(column_names)
    if os.path.exists('render_template.html'):
        print("file exists")

    return render_template('render_template.html', data=cpu_usage)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=1234)
