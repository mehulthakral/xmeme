from flask import Flask,render_template,jsonify,request,abort,Response,make_response
from flask_cors import CORS, cross_origin
import random
import pymysql
import requests
import json

app = Flask(__name__)
CORS(app)

# Endpoint to return swagger documentation as Json
@app.route('/swagger-ui/')
def get_swagger_doc():
    f = open('mehulthakral-xmeme_apis-1.0.0-swagger.json',) 
    data = json.load(f)
    return jsonify(data)

if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0', port=8080)