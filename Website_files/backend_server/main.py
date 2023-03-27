
from flask import Flask, request, redirect, url_for
from flask_cors import CORS, cross_origin
import time
app = Flask(__name__)
cors = CORS(app)

def simplyfy(text):
    time.sleep(5)
    return text.upper()

def detoxify(text):
    time.sleep(5)
    return text.lower()

@app.route('/')
def home():
   return 'Backend is running'
 
@app.route('/hello/<name>')
def hello_name(name):
   return 'Hello %s!' % name
 
@app.route('/getResult', methods=['POST'])
def login():
    print('loll')
    if request.method == 'POST':
        print(request.json['textToSimplify'])

        return simplyfy(request.json['textToSimplify'])
  
    else:
       return "Bad request"

@app.route('/getDResult', methods=['POST'])
def login2():
    print('loll')
    if request.method == 'POST':
         print(request.json['textToDetoxify'])

         return detoxify(request.json['textToDetoxify'])
  
    else:
       return "Bad request"
if __name__ == '__main__':
   app.run()