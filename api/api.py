# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 09:00:25 2020

@author: tebib
"""

import flask
from flask import request, jsonify
from flask import make_response
from flask import abort

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Create some test data for our catalog in the form of a list of dictionaries.
users = [
    {'id': 0,
     'username': 'shuya10',
     'email': 'shuya@gmail.com'},
    {'id': 1,
     'username': 'avinash10',
     'email': 'avi@mail.com'},
    {'id': 2,
     'username': 'sabri10',
     'email': 'sabri@yahoo.com'}
]

@app.route('/', methods=['GET'])
def home():
    return "<h1>DEV OPS PYTHON API</h1><p>Basic python api.</p>"

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

# A route to return all of the available entries in our catalog.
@app.route('/api/v1/users/all', methods=['GET'])
def api_all():
    return jsonify(users)

@app.route('/api/v1/users', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    # Create an empty list for our results
    results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    for user in users:
        if user['id'] == id:
            results.append(user)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)

@app.route('/api/v1/users', methods=['POST'])
def create_user():
    if not request.form or not 'username' in request.form:
        print(request.form)
        abort(400)
    user = {
        'id': users[-1]['id'] + 1,
        'username': request.form['username'],
        'email': request.form['email'],
        #'description': request.json.get('description', ""),
        #'done': False
    }
    users.append(user)
    return jsonify({'user': user}), 201


@app.route('/api/v1/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = [user for user in users if user['id'] == user_id]
    if len(user) == 0:
        abort(404)
    return jsonify({'user': user[0]})

@app.route('/api/v1/users/<int:user_id>', methods=['PUT'])
def update_task(user_id):
    print(1)
    user = [user for user in users if user['id'] == user_id]
    if len(user) == 0:
        abort(404)
    if not request.form:
        abort(400)
    if not request.form or not 'username' in request.form:
        abort(400)

    user[0]['username'] = request.form.get('username', user[0]['username'])
    user[0]['email'] = request.form.get('email', user[0]['email'])
    
    return jsonify({'user': user[0]})

@app.route('/api/v1/users/<int:id>', methods=['DELETE'])
def delete_task(user_id):
    user = [user for user in users if user['id'] == user_id]
    if len(user) == 0:
        abort(404)
    users.remove(user[0])
    return jsonify({'result': True})


if __name__ == '__main__':
     app.run(port='8080',debug=False)