

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



@app.route('/')
def my_form3():
    return render_template('faculty.html')


@app.route('/newfaculty', methods=['POST', 'GET'])  # name of form
def facultysignin():
    firebase = pyrebase.initialize_app(firebaseConfig)
    auth = firebase.auth()
    email = request.form['EMAIL']
    email = email.lower()
    facultysignin.email = email.title()
    password = request.form['PASSWORD']
    login = auth.sign_in_with_email_and_password(email, password)

    # cred = credentials.Certificate('firebase-sdk.json')
    # firebase_admin.initialize_app(cred)

    db = firestore.client()
    userid = ''
    if 'Fisk.Edu' in facultysignin.email:
        for i in facultysignin.email:
            if i != '@':
                userid = userid + i
            elif i == '@':
                break
    # print(userid)

    result = db.collection('FacultyandStaff').document(str(userid)).get()
    result = result.to_dict()
    first_name = result.get("First Name")
    first_name = first_name.lower()
    facultysignin.first_name = first_name.title()
    last_name = result.get("Last Name")
    last_name = last_name.lower()
    last_name = last_name.title()
    facultysignin.last_name = last_name.title()
    email = result.get("Email")
    email = email.lower()
    facultysignin.email = email.title()

    return render_template('facultypage.html', firstname=facultysignin.first_name, lastname=facultysignin.last_name,
                           fiskemail=facultysignin.email), dict(userid=userid)

    facultysignin()


@app.route('/retrievedata')
def facultyretrievedata():
    return render_template("dataoptions.html")
    facultyretrievedata()


@app.route('/group_data')
def groupretrievedata():
    return render_template("groupstudentchecker.html")
    groupretrievedata()


@app.route('/groupstudentchecker', methods=['POST', 'GET'])  # name of form
def groupdatareport():
    count = 0
    usernames = []
    docs = db.collection('student').get()
    year = request.form.get("YEAR")
    semester = request.form.get("SEMESTER")
    oppurtunity = request.form.get("OPPURTUNITY")
    if oppurtunity == "Undergraduate: Internship Opportunity":
        documentname = semester + " Internship Information"
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
                docs = doc_ref.collection(str(year)).document(str(documentname)).get()
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
                    finaltable = tabulate(table, tablefmt="html")
                    with open('../../Users/kehindeadekoya/PycharmProjects/pythonProject/templates/table.html', 'w') as f:
                        f.write(tabulate(table, tablefmt="html"))
                    with open('../../Users/kehindeadekoya/PycharmProjects/pythonProject/templates/table.html', 'r') as infile, open(
                            '/Users/kehindeadekoya/PycharmProjects/ocpdhub/templates/groupstudentresultspage.html',
                            'r') as infile2, open(
                        '../../Users/kehindeadekoya/PycharmProjects/pythonProject/templates/studentgroupdatareport.html', 'w') as outfile:
                        for line in infile2:
                            outfile.write(line)
                        for line in infile:
                            outfile.write(line)
    if oppurtunity == "Undergraduate: Research Experience":
        documentname = semester + " Research Experience Information"
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
            table = [['Student Username', 'First Name', 'Last Name', 'Fisk Email', 'Classification', 'Year',
                      'University Name', 'Program Name', 'Research Topic', 'Research Stipend',
                      'Attended Research Conference']]

            for user in usernames:
                doc_ref = db.collection('student').document(str(user))
                docs = doc_ref.collection(str(year)).document(str(documentname)).get()
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
                    order = [3, 8, 6, 7, 10, 0, 1, 4, 2, 5, 9, ]
                    dict = {'Student Username': user, 'First Name': first_name, 'Last Name': last_name,
                            'Fisk Email': fisk_email}
                    dict.update(docs)
                    for key in dict.items():
                        list.append(key)
                        list.sort(reverse=True)
                    # print(list)
                    list = [list[i] for i in order]
                    print(list)

                    for i in list:
                        newlist.append(i[1])
                    table.append(newlist)
                    finaltable = tabulate(table, tablefmt="html")
                    with open('../../Users/kehindeadekoya/PycharmProjects/pythonProject/templates/table.html', 'w') as f:
                        f.write(tabulate(table, tablefmt="html"))
                    with open('../../Users/kehindeadekoya/PycharmProjects/pythonProject/templates/table.html', 'r') as infile, open(
                            '/Users/kehindeadekoya/PycharmProjects/ocpdhub/templates/groupstudentresultspage.html',
                            'r') as infile2, open(
                        '../../Users/kehindeadekoya/PycharmProjects/pythonProject/templates/studentgroupdatareport.html', 'w') as outfile:
                        for line in infile2:
                            outfile.write(line)
                        for line in infile:
                            outfile.write(line)
    if oppurtunity == "Post Graduate: Full Time Opportunity":
        documentname = "Full-Time Information"
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
            table = [['Student Username', 'First Name', 'Last Name', 'Fisk Email', 'Personal Email', 'Year',
                      'Company Name', 'Position', 'Salary']]
            # print(len(table[0]))
            for user in usernames:
                doc_ref = db.collection('student').document(str(user))
                docs = doc_ref.collection(str(year)).document(str(documentname)).get()
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
                    order = [1, 7,5, 6, 4, 0, 8, 3, 2]
                    dict = {'Student Username': user, 'First Name': first_name, 'Last Name': last_name,
                            'Fisk Email': fisk_email}
                    dict.update(docs)
                    for key in dict.items():
                        list.append(key)
                        list.sort(reverse=True)
                    # print(list)
                    list = [list[i] for i in order]
                    print(list)

                    for i in list:
                        newlist.append(i[1])
                    table.append(newlist)
                    finaltable = tabulate(table, tablefmt="html")
                    with open('../../Users/kehindeadekoya/PycharmProjects/pythonProject/templates/table.html', 'w') as f:
                        f.write(tabulate(table, tablefmt="html"))
                    with open('../../Users/kehindeadekoya/PycharmProjects/pythonProject/templates/table.html', 'r') as infile, open(
                            '/Users/kehindeadekoya/PycharmProjects/ocpdhub/templates/groupstudentresultspage.html',
                            'r') as infile2, open(
                        '../../Users/kehindeadekoya/PycharmProjects/pythonProject/templates/studentgroupdatareport.html', 'w') as outfile:
                        for line in infile2:
                            outfile.write(line)
                        for line in infile:
                            outfile.write(line)
    if oppurtunity == "Post Graduate: Part Time Opportunity":
        documentname = "Part-Time Information"
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
            table = [['Student Username', 'First Name', 'Last Name', 'Fisk Email', 'Personal Email', 'Year',
                      'Company Name', 'Position', 'Hourly Pay']]
            # print(len(table[0]))
            for user in usernames:
                doc_ref = db.collection('student').document(str(user))
                docs = doc_ref.collection(str(year)).document(str(documentname)).get()
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
                    order = [1, 7, 4, 6, 3, 0, 8, 2, 5]
                    dict = {'Student Username': user, 'First Name': first_name, 'Last Name': last_name,
                            'Fisk Email': fisk_email}
                    dict.update(docs)
                    for key in dict.items():
                        list.append(key)
                        list.sort(reverse=True)
                    # print(list)
                    list = [list[i] for i in order]
                    print(list)

                    for i in list:
                        newlist.append(i[1])
                    table.append(newlist)
                    finaltable = tabulate(table, tablefmt="html")
                    with open('../../Users/kehindeadekoya/PycharmProjects/pythonProject/templates/table.html', 'w') as f:
                        f.write(tabulate(table, tablefmt="html"))
                    with open('../../Users/kehindeadekoya/PycharmProjects/pythonProject/templates/table.html', 'r') as infile, open(
                            '/Users/kehindeadekoya/PycharmProjects/ocpdhub/templates/groupstudentresultspage.html',
                            'r') as infile2, open(
                        '../../Users/kehindeadekoya/PycharmProjects/pythonProject/templates/studentgroupdatareport.html', 'w') as outfile:
                        for line in infile2:
                            outfile.write(line)
                        for line in infile:
                            outfile.write(line)

    if oppurtunity == "Post Graduate: Military Opportunity":
        documentname = "Military Service Information"
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
            table = [['Student Username', 'First Name', 'Last Name', 'Fisk Email', 'Personal Email', 'Year', 'Branch',
                      'Position', 'Hourly Pay']]
            # print(len(table[0]))
            for user in usernames:
                doc_ref = db.collection('student').document(str(user))
                docs = doc_ref.collection(str(year)).document(str(documentname)).get()
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
                    order = [1, 7, 5, 6, 3, 0, 8, 2, 4]
                    dict = {'Student Username': user, 'First Name': first_name, 'Last Name': last_name,
                            'Fisk Email': fisk_email}
                    dict.update(docs)
                    for key in dict.items():
                        list.append(key)
                        list.sort(reverse=True)
                    # print(list)
                    list = [list[i] for i in order]
                    print(list)

                    for i in list:
                        newlist.append(i[1])
                    table.append(newlist)
                    finaltable = tabulate(table, tablefmt="html")
                    with open('../../Users/kehindeadekoya/PycharmProjects/pythonProject/templates/table.html', 'w') as f:
                        f.write(tabulate(table, tablefmt="html"))
                    with open('../../Users/kehindeadekoya/PycharmProjects/pythonProject/templates/table.html', 'r') as infile, open(
                            '/Users/kehindeadekoya/PycharmProjects/ocpdhub/templates/groupstudentresultspage.html',
                            'r') as infile2, open(
                        '../../Users/kehindeadekoya/PycharmProjects/pythonProject/templates/studentgroupdatareport.html', 'w') as outfile:
                        for line in infile2:
                            outfile.write(line)
                        for line in infile:
                            outfile.write(line)
    if oppurtunity == "Post Graduate: Graduate School Opportunity":
        documentname = "Graduate School Information"
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
            table = [['Student Username', 'First Name', 'Last Name', 'Fisk Email', 'Personal Email', 'Year',
                      'University Name', 'Program Name', 'Degree']]
            # print(len(table[0]))
            for user in usernames:
                doc_ref = db.collection('student').document(str(user))
                docs = doc_ref.collection(str(year)).document(str(documentname)).get()
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
                    order = [1, 7, 4, 6, 3, 0, 5, 2, 8]
                    dict = {'Student Username': user, 'First Name': first_name, 'Last Name': last_name,
                            'Fisk Email': fisk_email}
                    dict.update(docs)
                    for key in dict.items():
                        list.append(key)
                        list.sort(reverse=True)
                    # print(list)
                    list = [list[i] for i in order]
                    print(list)

                    for i in list:
                        newlist.append(i[1])
                    table.append(newlist)

                    with open('../../Users/kehindeadekoya/PycharmProjects/pythonProject/templates/table.html', 'w') as f:
                        f.write(tabulate(table, tablefmt="html"))
                    with open('../../Users/kehindeadekoya/PycharmProjects/pythonProject/templates/table.html', 'r') as infile, open(
                            '/Users/kehindeadekoya/PycharmProjects/ocpdhub/templates/groupstudentresultspage.html',
                            'r') as infile2, open(
                        '../../Users/kehindeadekoya/PycharmProjects/pythonProject/templates/studentgroupdatareport.html', 'w') as outfile:
                        for line in infile2:
                            outfile.write(line)
                        for line in infile:
                            outfile.write(line)
    return render_template("studentgroupdatareport.html")


# if __name__ == "__main__":
#     app.run(debug=True)