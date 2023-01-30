
# from tester import groupdatareport
from flask import Flask, render_template, request

from flask import Flask, redirect, url_for, render_template, request

from flask import redirect
from pyrebase import pyrebase
import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from firebase_admin import firestore
import smtplib
import pandas as pd
from tabulate import tabulate


firebaseConfig = {
    "apiKey": "AIzaSyB9DaUxj2YCDMrNTOSgxpF49e6B5lCgOMA",
    "authDomain": "datahub-21e7e.firebaseapp.com",
    "databaseURL": "https://datahub-21e7e-default-rtdb.firebaseio.com",
    "projectId": "datahub-21e7e",
    "storageBucket": "datahub-21e7e.appspot.com",
    "messagingSenderId": "166143497203",
    "appId": "1:166143497203:web:4cf11ad5cfec0214ee7886",
    "measurementId": "G-6Z3W87LP23"
}

app = Flask(__name__)
app.config['SERVER_NAME'] = 'localhost:5000'


# defining the url or route for the website
#@app.route('/fiskocpddatahub')
cred = credentials.Certificate('firebase-sdk.json')
firebase_admin.initialize_app(cred)

db = firestore.client()
def group():
    usernames = []
    year = '2021'
    semester = "Winter"
    Opportunity = "Undergraduate: Internship Opportunity"
    docs = db.collection('student').get()
    if Opportunity == "Undergraduate: Internship Opportunity" and semester == "Winter":
        for doc in docs:
            doc = doc.to_dict()
            email = doc['Email']
            # print(email)
            if 'My.Fisk.Edu' in email:
                userid = ''
                for i in email:
                    if i != '@':
                        userid = userid + i
                    elif i == '@':
                        break
            usernames.append(userid)

            table = [['Student Username', 'First Name', 'Last Name', 'Fisk Email', 'Classification', 'Internship Year',
                      'Company Name', 'Position', 'Hourly Pay']]
            for user in usernames:
                doc_ref = db.collection('student').document(str(user))
                docs = doc_ref.collection(str(year)).document("Winter Internship Information").get()
                docs = docs.to_dict()
                result = db.collection('student').document(str(user)).get()
                result = result.to_dict()
                first_name = result.get('First Name')
                first_name = first_name.lower()
                first_name = first_name.title()
                last_name = result.get('Last Name')
                last_name = last_name.lower()
                last_name = last_name.title()
                fisk_email = result.get('Email')
                # print(fisk_email)
                newlist = []
                if docs:
                    order = {}
                    list = []
                    newlist = []
                    order = [0, 6, 2, 5, 8, 3, 7, 1, 4]
                    dict = {'Student Username': user, 'First Name': first_name, 'Last Name': last_name,
                            'Fisk Email': fisk_email}
                    dict.update(docs)
                    for key in dict.items():
                        list.append(key)
                        list.sort(reverse=True)
                    # print(list)
                    list = [list[i] for i in order]

                    for i in list:
                        newlist.append(i[1])
                    table.append(newlist)
            # print(headers)
            finaltable = tabulate(table, tablefmt="simple")
            print(finaltable)

    if Opportunity == "Undergraduate: Internship Opportunity" and semester == "Spring":
        for doc in docs:
            doc = doc.to_dict()
            email = doc['Email']
            # print(email)
            if 'My.Fisk.Edu' in email:
                userid = ''
                for i in email:
                    if i != '@':
                        userid = userid + i
                    elif i == '@':
                        break
            usernames.append(userid)

            table = [['Student Username', 'First Name', 'Last Name', 'Fisk Email', 'Classification', 'Internship Year',
                      'Company Name', 'Position', 'Hourly Pay']]
            for user in usernames:
                doc_ref = db.collection('student').document(str(user))
                docs = doc_ref.collection(str(year)).document("Spring Internship Information").get()
                docs = docs.to_dict()
                result = db.collection('student').document(str(user)).get()
                result = result.to_dict()
                first_name = result.get('First Name')
                first_name = first_name.lower()
                first_name = first_name.title()
                last_name = result.get('Last Name')
                last_name = last_name.lower()
                last_name = last_name.title()
                fisk_email = result.get('Email')
                # print(fisk_email)
                newlist = []
                if docs:
                    order = {}
                    list = []
                    newlist = []
                    order = [0, 6, 2, 5, 8, 3, 7, 1, 4]
                    dict = {'Student Username': user, 'First Name': first_name, 'Last Name': last_name,
                            'Fisk Email': fisk_email}
                    dict.update(docs)
                    for key in dict.items():
                        list.append(key)
                        list.sort(reverse=True)
                    # print(list)
                    list = [list[i] for i in order]

                    for i in list:
                        newlist.append(i[1])
                    table.append(newlist)
            # print(headers)
            finaltable = tabulate(table, tablefmt="html")
            print(finaltable)

    if Opportunity == "Undergraduate: Internship Opportunity" and semester == "Summer":
        for doc in docs:
            doc = doc.to_dict()
            email = doc['Email']
            # print(email)
            if 'My.Fisk.Edu' in email:
                userid = ''
                for i in email:
                    if i != '@':
                        userid = userid + i
                    elif i == '@':
                        break
            usernames.append(userid)

            table = [['Student Username', 'First Name', 'Last Name', 'Fisk Email', 'Classification', 'Internship Year',
                      'Company Name', 'Position', 'Hourly Pay']]
            for user in usernames:
                doc_ref = db.collection('student').document(str(user))
                docs = doc_ref.collection(str(year)).document("Summer Internship Information").get()
                docs = docs.to_dict()
                result = db.collection('student').document(str(user)).get()
                result = result.to_dict()
                first_name = result.get('First Name')
                first_name = first_name.lower()
                first_name = first_name.title()
                last_name = result.get('Last Name')
                last_name = last_name.lower()
                last_name = last_name.title()
                fisk_email = result.get('Email')
                # print(fisk_email)
                newlist = []
                if docs:
                    order = {}
                    list = []
                    newlist = []
                    order = [0, 6, 2, 5, 8, 3, 7, 1, 4]
                    dict = {'Student Username': user, 'First Name': first_name, 'Last Name': last_name,
                            'Fisk Email': fisk_email}
                    dict.update(docs)
                    for key in dict.items():
                        list.append(key)
                        list.sort(reverse=True)
                    # print(list)
                    list = [list[i] for i in order]

                    for i in list:
                        newlist.append(i[1])
                    table.append(newlist)
            # print(headers)
            finaltable = tabulate(table, tablefmt="html")
            print(finaltable)

    if Opportunity == "Undergraduate: Internship Opportunity" and semester == "Fall":
        for doc in docs:
            doc = doc.to_dict()
            email = doc['Email']
            # print(email)
            if 'My.Fisk.Edu' in email:
                userid = ''
                for i in email:
                    if i != '@':
                        userid = userid + i
                    elif i == '@':
                        break
            usernames.append(userid)

            table = [['Student Username', 'First Name', 'Last Name', 'Fisk Email', 'Classification', 'Internship Year',
                      'Company Name', 'Position', 'Hourly Pay']]
            for user in usernames:
                doc_ref = db.collection('student').document(str(user))
                docs = doc_ref.collection(str(year)).document("Fall Internship Information").get()
                docs = docs.to_dict()
                result = db.collection('student').document(str(user)).get()
                result = result.to_dict()
                first_name = result.get('First Name')
                first_name = first_name.lower()
                first_name = first_name.title()
                last_name = result.get('Last Name')
                last_name = last_name.lower()
                last_name = last_name.title()
                fisk_email = result.get('Email')
                # print(fisk_email)
                newlist = []
                if docs:
                    order = {}
                    list = []
                    newlist = []
                    order = [0, 6, 2, 5, 8, 3, 7, 1, 4]
                    dict = {'Student Username': user, 'First Name': first_name, 'Last Name': last_name,
                            'Fisk Email': fisk_email}
                    dict.update(docs)
                    for key in dict.items():
                        list.append(key)
                        list.sort(reverse=True)
                    # print(list)
                    list = [list[i] for i in order]

                    for i in list:
                        newlist.append(i[1])
                    table.append(newlist)
            # print(headers)
            finaltable = tabulate(table, tablefmt="html")
            print(finaltable)
