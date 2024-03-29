
from flask import Flask, request, redirect, url_for
from detoxification_final import detoxification
from lexical_text_simplication_final import user_interface_function
from flask_cors import CORS, cross_origin
import time
app = Flask(__name__)
cors = CORS(app)

def simplyfy(text):
    toRet = user_interface_function(text)
    return toRet

def detoxify(text):
    resultToReturn = detoxification(text)
    return resultToReturn


@app.route('/')
def home():
   return 'Backend is running'
 
@app.route('/hello/<name>')
def hello_name(name):
   return 'Hello %s!' % name
 
@app.route('/getResult', methods=['POST'])
def simplifyText():
    print('loll')
    if request.method == 'POST':
        print(request.json['textToSimplify'])

        return simplyfy(request.json['textToSimplify'])
  
    else:
       return "Bad request"

@app.route('/getDResult', methods=['POST'])
def detoxifyText():
    print('loll')
    if request.method == 'POST':
         print(request.json['textToDetoxify'])

         return detoxify(request.json['textToDetoxify'])
  
    else:
       return "Bad request"
if __name__ == '__main__':
   app.run()