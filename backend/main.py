from flask import Flask,current_app,request,jsonify
from flask.globals import request
from flask.wrappers import Response
from flask_pymongo import PyMongo

app = Flask(__name__)

app.app_context().push()
app.config.from_envvar('env_var')
db = PyMongo(current_app).db

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/signup",methods = ['POST'])
def signUp():

    user_data = request.get_json()
    print(user_data)
    username = user_data["username"]
    password = user_data["password"]
    
    db.users.insert_one({"username":username,"password":password})
    return "done"