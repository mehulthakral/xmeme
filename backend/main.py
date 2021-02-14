from flask import Flask,render_template,jsonify,request,abort,Response,make_response
from flask_cors import CORS, cross_origin
import random
import pymysql
import requests

# Option to choose db - cloud db or on localhost

# db = pymysql.connect(host="us-cdbr-east-03.cleardb.com", user="b163ecafb050c5", password="67c0858d", db="heroku_82df1ddd3b24563")

db = pymysql.connect(host="localhost", user="root", password="", db="xmeme", port=3307)
# Also comment db in read and write fns

app = Flask(__name__)
CORS(app,allow_headers='*',origins='*')

# app.config['CORS_HEADERS'] = 'Origin, X-Requested-With, Content-Type, Accept'

# Option to choose backend - heroku or localhost
# backend_url = "https://mehul-xmeme-backend.herokuapp.com"
backend_url = "http://localhost:8081"

def _build_cors_prelight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "Content-Type")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "Origin, X-Requested-With, Content-Type, Accept")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

# Endpoint for adding memes to the backend
@app.route('/memes',methods=["POST"])
def submit_meme():

    # if request.method == "OPTIONS": # CORS preflight
    #     return _build_cors_prelight_response()

    global backend_url
    json = request.get_json()

    print(json)

    # Code to check if the meme already exists
    inp={"table":"MEMES","columns":["id","name","url","caption"],"where":"url='"+json["url"]+"'"}
    send=requests.post(backend_url+'/api/v1/db/read',json=inp)
    res=eval(send.content)
    if(len(res)!=0):
        return Response("Meme already exists",status=409,mimetype="application/text")
        # return _corsify_actual_response(Response("Meme already exists",status=409,mimetype="application/text"))

    # Code to insert meme info to the db
    inp={"table":"MEMES","columns":["name","url","caption"],"data":[json["name"],json["url"],json["caption"]],"type":"insert"}
    send=requests.post(backend_url+'/api/v1/db/write',json=inp)
    send.json()

    # Code to get the id allocated by the db for the added meme 
    inp={"table":"MEMES","columns":["id"],"where":"name='"+json["name"]+"' AND url='"+json["url"]+"' AND caption='"+json["caption"]+"'"}
    send=requests.post(backend_url+'/api/v1/db/read',json=inp)
    res=eval(send.content)

    return jsonify({"id":str(res[0][0])})
    # return _corsify_actual_response(jsonify({"id":str(res[0][0])}))

# Endpoint to return latest memes based on max 'count' number of memes 
@app.route('/memes/max/<count>',methods=["GET"])
@app.route('/memes',methods=["GET"])
def get_memes(count=100):

    global backend_url

    # Code to fetch memes from the db
    inp={"table":"MEMES","columns":["id","name","url","caption"],"where":"","orderBy":"time DESC"}
    send=requests.post(backend_url+'/api/v1/db/read',json=inp)
    res=eval(send.content)

    # Constructing response
    ans = []
    l = min(int(count),len(res))
    for i in range(l):
        temp = {}
        temp["id"]=str(res[i][0])
        temp["name"]=res[i][1]
        temp["url"]=res[i][2]
        temp["caption"]=res[i][3]
        ans.append(temp)

    return jsonify(ans)

# Endpoint to fetch details of a particular meme
@app.route('/memes/<id>',methods=["GET"])
def get_meme(id):
    
    print("Get Meme called")
    global backend_url
    
    # Code to fetch details of a particular meme
    inp={"table":"MEMES","columns":["id","name","url","caption"],"where":"id='"+id+"'"}
    send=requests.post(backend_url+'/api/v1/db/read',json=inp)
    res=eval(send.content)
    
    # Code to check if meme actually exists and constructing response
    if(len(res)!=0):
        temp = {}
        temp["id"]=res[0][0]
        temp["name"]=res[0][1]
        temp["url"]=res[0][2]
        temp["caption"]=res[0][3]
        return jsonify(temp)

    return Response("No meme found",status=404,mimetype="application/text")


# Endpoint to update details of a particular meme
@app.route('/memes/<id>',methods=["PATCH"])
@cross_origin(headers=['Content-Type'])
def update_meme(id):
    
    print("Update Meme called")
    global backend_url

    # Code to check if meme exists in the db
    json = request.get_json()
    inp={"table":"MEMES","columns":["id","name","url","caption"],"where":"id='"+id+"'"}
    send=requests.post(backend_url+'/api/v1/db/read',json=inp)
    res=eval(send.content)
    
    print(len(res))

    # If meme exists update the details and send the response
    if(len(res)!=0):
        inp={"table":"MEMES","columns":["url","caption"],"data":[json["url"],json["caption"]],"where":"id='"+id+"'","type":"update"}
        send=requests.post(backend_url+'/api/v1/db/write',json=inp)
        send.json()
        print("Response Sent")
        return Response("Updated successfully",status=200,mimetype="application/text")
        # return _corsify_actual_response(Response("Updated successfully",status=200,mimetype="application/text"))   

    # return _corsify_actual_response(Response("No meme found",status=404,mimetype="application/text"))
    return Response("No meme found",status=404,mimetype="application/text")


# Endpoint to make changes to db - insert, update, delete 
@app.route('/api/v1/db/write',methods=["POST"])
def write_db():

    json = request.get_json()
    # db = pymysql.connect(host="us-cdbr-east-03.cleardb.com", user="b163ecafb050c5", password="67c0858d", db="heroku_82df1ddd3b24563")
    cur = db.cursor()

    if(json["type"]=="insert"):

        columns = json["columns"][0]
        data = "'"+json["data"][0]+"'"

        for iter in range(1,len(json["columns"])):
            columns = columns + "," + json["columns"][iter]
            data = data + ",'" + json["data"][iter]+"'"

        sql = "INSERT INTO "+json["table"]+"("+columns+") VALUES ("+data+")"

    elif(json["type"]=="delete"):

        if json["where"]!="":
            sql = "DELETE FROM "+json["table"]+" WHERE "+json["where"]
        else:
            sql = "DELETE FROM "+json["table"]

    elif(json["type"]=="update"):

        string = json["columns"][0] + "='" + json["data"][0] + "'"

        for iter in range(1,len(json["columns"])):
            string = string + ", " + json["columns"][iter] + "='" + json["data"][iter] + "'"

        sql = "UPDATE "+json["table"]+" SET "+ string + " WHERE " + json["where"] 

    cur.execute(sql)
    db.commit()
    cur.close()

    return Response("1",status=200,mimetype="application/text")

# Endpoint to read data from the db
@app.route('/api/v1/db/read',methods=["POST"])
def read_db():

    json = request.get_json()
    # db = pymysql.connect(host="us-cdbr-east-03.cleardb.com", user="b163ecafb050c5", password="67c0858d", db="heroku_82df1ddd3b24563")
    cur = db.cursor()
    
    columns = json["columns"][0]
    for iter in range(1,len(json["columns"])):
        columns = columns + "," + json["columns"][iter]

    if json["where"]!="":
        sql = "SELECT "+columns+" FROM "+json["table"]+" WHERE "+json["where"]
    else:
        sql = "SELECT "+columns+" FROM "+json["table"]

    if "orderBy" in json:
        sql = sql + " ORDER BY " + json["orderBy"]

    cur.execute(sql)
    results = cur.fetchall()
    results = list(map(list,results))
    cur.close()

    return Response(str(results),status=200,mimetype="application/text")

if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0', port=8081)
