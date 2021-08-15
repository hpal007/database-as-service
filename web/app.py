from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)
client = MongoClient("mongodb://db:27017")
db= client.SentencesDatabase
users = db["Users"]


def verifyUser(username, password):
    
    hashed_pw = users.find({"Username": username})[0]["Password"]
    if bcrypt.checkpw(password.encode('utf8'), hashed_pw):
        return True
    else:
        return False

def get_token_count(username):

    token = users.find({"Username": username})[0]["Token"]
    return token

def get_sentence(username):

    sentence = users.find({"Username": username})[0]["Sentence"]
    return sentence

class Regiester(Resource):
    def post(self):

        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["password"]
        hash_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        users.insert_one({
            "Username": username, 
            "Password": hash_pw,
            "Sentence": "", 
            "Token": 5})

        retJson = {
            "status": 200,
            "msg": "You successfully signed up for the API"
        }
        return jsonify(retJson)

class StoreSentence(Resource):
    def post(self):

        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["password"]
        sentences = postedData["sentences"]
        correct_pw =  verifyUser(username,password)

        if not correct_pw:
            returnJson = {
                "status_code": 302,
                "msg": "You are not a valid user, try creating account first!!."
            }
            return jsonify(returnJson)

        no_of_token = get_token_count(username)
        if no_of_token ==0:
            returnJson = {
                "status_code": 301,
                "msg": "You are out of token, buy to use more."
            }
            return jsonify(returnJson)
        token =no_of_token -1
        returnJson = {
                "status_code": 200,
                "token_remaining": token,
                "msg": "Your sentence has been successfully uploaded."
            }

        users.update_one({
            "Username": username
        },{
            "$set":{
                "Sentence": sentences,
                "Token": token
            }
        })
        return jsonify(returnJson)
 

class RetriveData(Resource):
    def post(self):
        
        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["password"]
 
        correct_pw =  verifyUser(username,password)

        if not correct_pw:
            returnJson = {
                "status_code": 302,
                "msg": "You are not a valid user, try creating account first!!."
            }
            return jsonify(returnJson)

        no_of_token = get_token_count(username)
        if no_of_token ==0:
            returnJson = {
                "status_code": 301,
                "msg": "You are out of token, buy to use more."
            }
            return jsonify(returnJson)

        token =no_of_token -1
        users.update_one({
            "Username": username
        },{
            "$set":{
                "Token": token
            }
        })
        returnJson = {
                "status_code": 200,
                "sentence": get_sentence(username),
                "token_remaining": token
            }
        return jsonify(returnJson)

api.add_resource(Regiester,'/register')
api.add_resource(StoreSentence,'/store')
api.add_resource(RetriveData, '/get')


@app.route('/')
def hello_world():
    return "Wellcome!"



if __name__=="__main__":
    app.run(debug=True)



'''
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient

app = Flask(__name__)

api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.aNewDB
UserNum = db["UserNum"]
UserNum.insert({
    "no_of_user":0,

})

class Visit(Resource):
    def get(self):
        prev_num = UserNum.find({})[0]['no_of_user']
        new_num = prev_num + 1
        UserNum.update({},{"$set":{"no_of_user":new_num}})
        return str("Hello user" + str(new_num))


def checkPostedData(postedData, functionName):
    if (functionName == "add" or functionName == "subtract" or functionName == "multiply"):
        if "x" not in postedData or "y" not in postedData:
            return 301 #Missing parameter
        else:
            return 200
    elif (functionName == "division"):
        if "x" not in postedData or "y" not in postedData:
            return 301
        elif int(postedData["y"])==0:
            return 302
        else:
            return 200

class Add(Resource):
    def post(self):
        #If I am here, then the resouce Add was requested using the method POST

        #Step 1: Get posted data:
        postedData = request.get_json()

        #Steb 1b: Verify validity of posted data
        status_code = checkPostedData(postedData, "add")
        if (status_code!=200):
            retJson = {
                "Message": "An error happened",
                "Status Code":status_code
            }
            return jsonify(retJson)

        #If i am here, then status_code == 200
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)

        #Step 2: Add the posted data
        ret = x+y
        retMap = {
            'Message': ret,
            'Status Code': 200
        }
        return jsonify(retMap)

class Subtract(Resource):
    def post(self):
        #If I am here, then the resouce Subtract was requested using the method POST

        #Step 1: Get posted data:
        postedData = request.get_json()

        #Steb 1b: Verify validity of posted data
        status_code = checkPostedData(postedData, "subtract")


        if (status_code!=200):
            retJson = {
                "Message": "An error happened",
                "Status Code":status_code
            }
            return jsonify(retJson)

        #If i am here, then status_code == 200
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)

        #Step 2: Subtract the posted data
        ret = x-y
        retMap = {
            'Message': ret,
            'Status Code': 200
        }
        return jsonify(retMap)

class Multiply(Resource):
    def post(self):
        #If I am here, then the resouce Multiply was requested using the method POST

        #Step 1: Get posted data:
        postedData = request.get_json()

        #Steb 1b: Verify validity of posted data
        status_code = checkPostedData(postedData, "multiply")


        if (status_code!=200):
            retJson = {
                "Message": "An error happened",
                "Status Code":status_code
            }
            return jsonify(retJson)

        #If i am here, then status_code == 200
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)

        #Step 2: Multiply the posted data
        ret = x*y
        retMap = {
            'Message': ret,
            'Status Code': 200
        }
        return jsonify(retMap)

class Divide(Resource):
    def post(self):
        #If I am here, then the resouce Divide was requested using the method POST

        #Step 1: Get posted data:
        postedData = request.get_json()

        #Steb 1b: Verify validity of posted data
        status_code = checkPostedData(postedData, "division")


        if (status_code!=200):
            retJson = {
                "Message": "An error happened",
                "Status Code":status_code
            }
            return jsonify(retJson)

        #If i am here, then status_code == 200
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)

        #Step 2: Multiply the posted data
        ret = (x*1.0)/y
        retMap = {
            'Message': ret,
            'Status Code': 200
        }
        return jsonify(retMap)



api.add_resource(Add, "/add")
api.add_resource(Subtract, "/subtract")
api.add_resource(Multiply, "/multiply")
api.add_resource(Divide, "/division")
api.add_resource(Visit,"/hello")
@app.route('/')
def hello_world():
    return "Hello World!"


if __name__=="__main__":
    app.run(debug=True, port=9091, host='0.0.0.0')


'''