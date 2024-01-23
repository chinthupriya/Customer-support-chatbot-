import json
from difflib import get_close_matches
#from sklearn.feature_extraction.text import TfidfVectorizer
#from sklearn.model_selection import train_test_split as ttsplit
#from sklearn import svm
import pandas as pd
import pickle
import numpy as np
from datetime import datetime
from flask import Flask, render_template, redirect, request, session, url_for
from flask import Flask, render_template
import firebase_admin
import random
from firebase_admin import credentials
import os
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
from google.cloud.firestore_v1 import FieldFilter
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
#from chatterbot import ChatBot
#from chatterbot.trainers import ListTrainer
# Create a new chat bot named Charlie
#chatbot = ChatBot('FreeBirdsBot')
#trainer = ListTrainer(chatbot)
#trainer.train(['Hi','Hello','How are you?','I am fine and You?','Greate','What are you Doing?','nothing just roaming around.'])

cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred)
app = Flask(__name__)

app.secret_key="CustomerSuport@1234"
app.config['upload_folder']='/static/upload'

@app.route('/')
def homepage():
    try:
        return render_template("index.html")
    except Exception as e:
        return str(e)

@app.route('/index')
def indexpage():
    try:
        return render_template("index.html")
    except Exception as e:
        return str(e)

@app.route('/logout')
def logoutpage():
    try:
        return render_template("index.html")
    except Exception as e:
        return str(e)

@app.route('/about')
def aboutpage():
    try:
        return render_template("about.html")
    except Exception as e:
        return str(e)

@app.route('/logout')
def logout():
    try:
        return render_template("index.html")
    except Exception as e:
        return str(e)

@app.route('/adminmainpage')
def adminmainpage():
    try:
        return render_template("adminmainpage.html")
    except Exception as e:
        return str(e)

@app.route('/services')
def servicespage():
    try:
        return render_template("services.html")
    except Exception as e:
        return str(e)

@app.route('/gallery')
def gallerypage():
    try:
        return render_template("gallery.html")
    except Exception as e:
        return str(e)

@app.route('/adminviewstaffs')
def adminviewstaffspage():
    try:
        db = firestore.client()
        newstaff_ref = db.collection('newstaff')
        staffdata = newstaff_ref.get()
        data=[]
        for doc in staffdata:
            print(doc.to_dict())
            print(f'{doc.id} => {doc.to_dict()}')
            data.append(doc.to_dict())
        print("Staff Data " , data)
        return render_template("adminviewstaffs.html", data=data)
    except Exception as e:
        return str(e)

@app.route('/adminviewusers')
def adminviewuserspage():
    try:
        db = firestore.client()
        dbref = db.collection('newuser')
        userdata = dbref.get()
        data = []
        for doc in userdata:
            print(doc.to_dict())
            print(f'{doc.id} => {doc.to_dict()}')
            data.append(doc.to_dict())
        print("Staff Data ", data)
        return render_template("adminviewusers.html", data=data)
    except Exception as e:
        return str(e)

@app.route('/adminviewcontacts')
def adminviewcontacts():
    try:
        db = firestore.client()
        dbref = db.collection('newcontact')
        userdata = dbref.get()
        data = []
        for doc in userdata:
            print(doc.to_dict())
            print(f'{doc.id} => {doc.to_dict()}')
            data.append(doc.to_dict())
        return render_template("adminviewcontacts.html", data=data)
    except Exception as e:
        return str(e)

@app.route('/userviewchats')
def userviewchats():
    try:
        db = firestore.client()
        dbref = db.collection('newchat')
        userdata = dbref.get()
        data = []
        userid = session['userid']
        for doc in userdata:
            #print(doc.to_dict())
            #print(f'{doc.id} => {doc.to_dict()}')
            temp=doc.to_dict()
            if(temp['UserId']==userid and temp['Flag']==True):
                data.append(doc.to_dict())
        return render_template("userviewchats.html", data=data)
    except Exception as e:
        return str(e)

@app.route('/adminviewchats')
def adminviewchats():
    try:
        db = firestore.client()
        dbref = db.collection('newchat')
        userdata = dbref.get()
        data = []
        for doc in userdata:
            #print(doc.to_dict())
            #print(f'{doc.id} => {doc.to_dict()}')
            if(doc.to_dict()['Flag']==True):
                data.append(doc.to_dict())
        return render_template("adminviewchats.html", data=data)
    except Exception as e:
        return str(e)

@app.route('/adminviewunanswered')
def adminviewunanswered():
    try:
        db = firestore.client()
        dbref = db.collection('newchat')
        userdata = dbref.get()
        data = []
        for doc in userdata:
            temp=doc.to_dict()
            if(temp['Flag']==False):
                data.append(doc.to_dict())
        return render_template("adminviewunanswered.html", data=data)
    except Exception as e:
        return str(e)

@app.route('/adminviewunanswered1')
def adminviewunanswered1():
    try:
        args = request.args
        id = args['id']
        db = firestore.client()
        dbref = db.collection('newchat')
        userdata = dbref.get()
        data = []
        userid=None
        for doc in userdata:
            temp=doc.to_dict()
            if(temp['id']==id):
                data=temp
                userid=temp['UserId']
                break
        dbref = db.collection('newuser')
        temp = dbref.document(userid).get().to_dict()
        return render_template("adminviewunanswered1.html", data=data, userdata=temp)
    except Exception as e:
        return str(e)

@app.route('/adminviewunanswered2',methods=["POST","GET"])
def adminviewunanswered2():
    try:
        if request.method == 'POST':
            answerid = request.form['id']
            answer= request.form['answer']
            db = firestore.client()
            dbref = db.collection('newchat')
            doc = dbref.document(answerid)
            field_updates = {"Flag": True,'Answer':answer}
            doc.update(field_updates)
            #print("Document : ", doc, " Question : ", doc.to_dict()['Question'])
        return redirect(url_for("adminviewchats"))
    except Exception as e:
        return str(e)

@app.route('/adminlogin',methods=["POST","GET"])
def adminloginpage():
    try:
        if request.method == 'POST':
            uname = request.form['uname']
            pwd = request.form['pwd']
            if uname == "admin" and pwd == "admin":
                return render_template("adminmainpage.html")
            else:
                return render_template("adminlogin.html", msg="UserName/Password is Invalid")
        return render_template("adminlogin.html",msg="")
    except Exception as e:
        return str(e)

@app.route('/userlogincheck', methods=['POST'])
def userlogincheck():
    try:
        if request.method == 'POST':
            uname = request.form['uname']
            pwd = request.form['pwd']
            db = firestore.client()
            print("Uname : ", uname, " Pwd : ", pwd);
            newdb_ref = db.collection('newuser')
            dbdata = newdb_ref.get()
            data = []
            flag = False
            for doc in dbdata:
                #print(doc.to_dict())
                #print(f'{doc.id} => {doc.to_dict()}')
                #data.append(doc.to_dict())
                data = doc.to_dict()
                if(data['UserName']==uname and data['Password']==pwd):
                    flag=True
                    session['userid']=data['id']
                    break
            if(flag):
                print("Login Success")
                return render_template("usermainpage.html")
            else:
                return render_template("userlogin.html", msg="UserName/Password is Invalid")
    except Exception as e:
        return render_template("userlogin.html", msg=e)

@app.route('/stafflogincheck', methods=['POST'])
def stafflogincheck():
    try:
        if request.method == 'POST':
            uname = request.form['uname']
            pwd = request.form['pwd']
            db = firestore.client()
            print("Uname : ", uname, " Pwd : ", pwd);
            newdb_ref = db.collection('newstaff')
            dbdata = newdb_ref.get()
            data = []
            flag = False
            for doc in dbdata:
                data = doc.to_dict()
                if(data['UserName']==uname and data['Password']==pwd):
                    flag=True
                    session['staffid']=data['id']
                    break
            if(flag):
                print("Login Success")
                return render_template("staffmainpage.html")
            else:
                return render_template("stafflogin.html", msg="UserName/Password is Invalid")
    except Exception as e:
        return render_template("stafflogin.html", msg=e)

@app.route('/userlogin',methods=["POST","GET"])
def userloginpage():
    try:
        if request.method == 'POST':
            uname = request.form['uname']
            pwd = request.form['pwd']
            db = firestore.client()
            newdb_ref = db.collection('newuser')
            dbdata = newdb_ref.get()
            flag = False
            for doc in dbdata:
                data = doc.to_dict()
                if (data['UserName'] == uname and data['Password'] == pwd):
                    flag = True
                    session['userid'] = data['id']
                    break
            if (flag):
                print("Login Success")
                return render_template("usermainpage.html")
            else:
                return render_template("userlogin.html", msg="UserName/Password is Invalid")
        return render_template("userlogin.html")
    except Exception as e:
        return str(e)

@app.route('/stafflogin',methods=["POST","GET"])
def staffloginpage():
    try:
        return render_template("stafflogin.html")
    except Exception as e:
        return str(e)

@app.route('/newuser')
def newuser():
    try:
        msg=""
        return render_template("newuser.html", msg=msg)
    except Exception as e:
        return str(e)

@app.route('/addnewuser', methods=['POST',"GET"])
def addnewuser():
    try:
        print("Add New User page")
        if request.method == 'POST':
            fname = request.form['fname']
            lname = request.form['lname']
            uname = request.form['uname']
            pwd = request.form['pwd']
            email = request.form['email']
            phnum = request.form['phnum']
            address = request.form['address']
            id = str(random.randint(1000, 9999))
            json = {'id': id,
                    'FirstName': fname,'LastName':lname,
                    'UserName': uname,'Password':pwd,
                    'EmailId': email,'PhoneNumber':phnum,
                    'Address': address}
            db = firestore.client()
            newuser_ref = db.collection('newuser')
            id = json['id']
            newuser_ref.document(id).set(json)
        return render_template("newuser.html", msg="New User Added Success")
    except Exception as e:
        return str(e)

@app.route('/newstaff', methods=['POST',"GET"])
def newstaff():
    try:
        msg=""
        return render_template("adminaddstaff.html", msg=msg)
    except Exception as e:
        return str(e)

@app.route('/adminaddstaff', methods=['POST',"GET"])
def adminaddstaff():
    try:
        msg=""
        if request.method == 'POST':
            print("Add New Staff page")
            fname = request.form['fname']
            lname = request.form['lname']
            uname = request.form['uname']
            pwd = request.form['pwd']
            email = request.form['email']
            phnum = request.form['phnum']
            address = request.form['address']
            id = str(random.randint(1000, 9999))
            json = {'id': id,
                    'FirstName': fname,'LastName':lname,
                    'UserName': uname,'Password':pwd,
                    'EmailId': email,'PhoneNumber':phnum,
                    'Address': address}
            db = firestore.client()
            newuser_ref = db.collection('newstaff')
            id = json['id']
            newuser_ref.document(id).set(json)
            msg="New Staff Added Success"
            return render_template("adminaddstaff.html", msg=msg)
        else:
            return render_template("adminaddstaff.html", msg=msg)
    except Exception as e:
        return str(e)

@app.route('/contact',methods=['POST','GET'])
def contactpage():
    try:
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            subject = request.form['subject']
            message = request.form['message']
            id = str(random.randint(1000, 9999))
            json = {'id': id,
                    'ContactName': name,
                    'Message': message, 'Subject': subject,
                    'EmailId': email}
            db = firestore.client()
            db_ref = db.collection('newcontact')
            id = json['id']
            db_ref.document(id).set(json)
            msg="Contact Added Success"
            return render_template("contact.html",msg=msg)
        else:
            return render_template("contact.html")
    except Exception as e:
        return str(e)

@app.route('/userviewprofile')
def userviewprofile():
    try:
        id=session['userid']
        print("Id",id)
        db = firestore.client()
        newdb_ref = db.collection('newuser')
        data = newdb_ref.document(id).get().to_dict()
        print(data)
        return render_template("userviewprofile.html", data=data)
    except Exception as e:
        return str(e)
        return render_template("userviewprofile.html", msg=e)

@app.route('/staffviewprofile')
def staffviewprofile():
    try:
        id=session['staffid']
        print("Id",id)
        db = firestore.client()
        newdb_ref = db.collection('newstaff')
        data = newdb_ref.document(id).get().to_dict()
        print(data)
        return render_template("staffviewprofile.html", data=data)
    except Exception as e:
        return str(e)
        return render_template("stafflogin.html", msg=e)

brain = json.load(open('knowledge.json'))
@app.route('/userchatboot',methods=['POST','GET'])
def userchatboot():
    try:
        answer = ""
        if request.method == 'POST':
            usertext = request.form['usertext']
            usertext = usertext.lower()
            message = 'You: ' + usertext + '\n'
            answer=""
            close_match = get_close_matches(message, brain.keys())
            flag=False
            if close_match:
                reply = 'Chat Boot : ' + brain[close_match[0]][0] + '\n'
                answer=brain[close_match[0]][0]
                flag=True
            else:
                reply = 'Chat Boot : ' + 'Cant it in my knowledge base\n'
                answer = 'Cant it in my knowledge base'
            userid = session['userid']
            now = datetime.now()
            date_time = now.strftime("%d/%m/%Y %H:%M:%S")
            id = str(random.randint(1000, 9999))
            json = {'id': id,
                    'UserId': userid,
                    'Question': usertext,
                    'Answer': answer,
                    'DateTime': date_time,
                    'Flag':flag}
            answer = message + reply
            db = firestore.client()
            db_ref = db.collection('newchat')
            id = json['id']
            db_ref.document(id).set(json)
        return render_template("userchatboot.html", answer=answer)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.debug = True
    app.run()