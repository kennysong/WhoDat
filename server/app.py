import os
import jinja2
from flask import Flask, render_template, redirect, request
from flask.ext.pymongo import PyMongo

app = Flask(__name__)
app.config.update(
    DEBUG = True,
)

@app.route('/')
def home_page():
    # online_users = mongo.db.users.find({'': True})
    return "Who Dat?"

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port,debug=True)