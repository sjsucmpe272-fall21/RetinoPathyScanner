from fastai.basic_train import load_learner
from fastai.text import learner
from flask import Flask,current_app,request,jsonify
from flask.globals import request
from flask.wrappers import Response
from flask_pymongo import PyMongo
from dotenv import dotenv_values
from bson.json_util import dumps, loads
from flask_jwt import JWT, jwt_required, current_identity
import jwt
from fastai.vision import *
from flask_cors import CORS, cross_origin

app = Flask(__name__)

app.app_context().push()

cors = CORS(app)
config = dotenv_values(".env")
app.config['MONGO_URI'] = config["MONGO_URI"]
app.config["SECRET_KEY"] = config["SECRET_KEY"]
app.config['CORS_HEADERS'] = 'Content-Type'

path = Path("")

learner = load_learner(path,"model")
db = PyMongo(current_app).db


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/login",methods = ['POST'])
def login():
    print("hello")
    user_data = request.get_json(force=True)
    username = user_data["username"]
    password = user_data["password"]
    result = db.users.find_one({"username":username,"password":password})
    if(result == None):
        return "404"
    token = jwt.encode({"username" : result["username"]},app.config.get("SECRET_KEY"),algorithm="HS256").decode('utf-8')
    print(str(token))
    resp = {"response":{"username" : result["username"]},"token":token}

    return dumps(resp)


@app.route("/signup",methods = ['POST'])
def signUp():

    print(request)
    user_data = request.get_json(force=True)
    print(user_data)
    username = user_data["username"]
    password = user_data["password"]
	    
    db.users.insert_one({"username":username,"password":password})
    return "done"

@app.route("/checkImage",methods = ['POST'])
def checkImage():
    img = request.files.get("image")
    token = request.form.get("token")
    print(request)
    print("+++++++++")
    print(token)
    print(img)
    print("+++++++++")

    if(verify_user(token)):
        print("verified")
        res,probab = classify(img)
        print(res)
        ret_val = dumps({"result":res,"probab":probab})
        return ret_val
    if(verify_user(token))  :
        return classify(img)

def classify(img_path):
    
    img = open_image(img_path)
    pred_probab = str((max(learner.predict(img)[2])/(sum(learner.predict(img)[2]))).item())
    pred =str(learner.predict(img)[0])

    if(pred == "0"):
        return "Negligible Possibility",pred_probab
    if(pred == "1"):
        return "Mild Possibility",pred_probab
    if(pred == "2"):
        return "Moderate Possibility",pred_probab
    if(pred == "3"):
        return "Severe Possibility",pred_probab


    return "Please Try again later","NA"

def verify_user(token):
    try:
        jwt.decode(token,app.config.get("SECRET_KEY"),algorithm="HS256")
        return True
    except:
        return False
if __name__ == "__main__":
	app.run(host="0.0.0.0",port=5000,ssl_context='adhoc')

