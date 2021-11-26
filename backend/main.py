from fastai.basic_train import load_learner
from fastai.text import learner
from flask import Flask,current_app,request,jsonify
from flask.globals import request
from flask.wrappers import Response
from flask_pymongo import PyMongo
from dotenv import dotenv_values
from fastai.vision import *
app = Flask(__name__)

app.app_context().push()

config = dotenv_values(".env")
app.config['MONGO_URI'] = config["MONGO_URI"]

path = Path("")

learner = load_learner(path,"model")
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

@app.route("/checkImage",methods = ['POST'])
def checkImage():
    img = request.files.get("image")
    #print(img)
    return classify(img)

def classify(img_path):
    
    img = open_image(img_path)
    pred = str(learner.predict(img)[0])

    if(pred == "0"):
        return "Negligible Possibility"
    if(pred == "1"):
        return "Mild Possibility"
    if(pred == "2"):
        return "Moderate Possibility"
    if(pred == "3"):
        return "Severe Possibility"


    return "Please Try again later"