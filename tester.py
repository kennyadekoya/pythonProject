

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

# @app.route('/groupstudentchecker', methods=['POST', 'GET'])  # name of form
# def group():
#     db = firestore.client()
#     usernames = []
#     year = "2022"
#     semester = "Fall"
#     Opportunity = "Undergraduate: Internship Opportunity"
#     documentname = semester + " Internship Information"
#     # print(documentname)
#     docs = db.collection('student').get()
#     for doc in docs:
#         doc = doc.to_dict()
#         email = doc['Email']
#         # print(email)
#         if 'My.Fisk.Edu' in email:
#             userid = ''
#             for i in email:
#                 if i != '@':
#                     userid = userid + i
#                 elif i == '@':
#                     break
#         usernames.append(userid)
#
#         table = [['Student Username', 'First Name', 'Last Name', 'Fisk Email', 'Classification', 'Internship Year',
#                   'Company Name', 'Position', 'Hourly Pay']]
#         for user in usernames:
#             doc_ref = db.collection('student').document(str(user))
#             docs = doc_ref.collection(str(year)).document(str(documentname)).get()
#             docs = docs.to_dict()
#             result = db.collection('student').document(str(user)).get()
#             result = result.to_dict()
#             first_name = result.get('First Name')
#             first_name = first_name.lower()
#             first_name = first_name.title()
#             last_name = result.get('Last Name')
#             last_name = last_name.lower()
#             last_name = last_name.title()
#             fisk_email = result.get('Email')
#             # print(fisk_email)
#             newlist = []
#             if docs:
#                 order = {}
#                 list = []
#                 newlist = []
#                 order = [0, 6, 2, 5, 8, 3, 7, 1, 4]
#                 dict = {'Student Username': user, 'First Name': first_name, 'Last Name': last_name,
#                         'Fisk Email': fisk_email}
#                 dict.update(docs)
#                 for key in dict.items():
#                     list.append(key)
#                     list.sort(reverse=True)
#                 # print(list)
#                 list = [list[i] for i in order]
#
#                 for i in list:
#                     newlist.append(i[1])
#                 table.append(newlist)
#             finaltable = tabulate(table, tablefmt="simple")
#     print(finaltable)
#     return(finaltable)
#
# group()


# @app.route('/')
# def my_form3():
#     return render_template('faculty.html')
#
#
# @app.route('/newfaculty', methods=['POST', 'GET'])  # name of form
# def facultysignin():
#     firebase = pyrebase.initialize_app(firebaseConfig)
#     auth = firebase.auth()
#     email = request.form['EMAIL']
#     email = email.lower()
#     facultysignin.email = email.title()
#     password = request.form['PASSWORD']
#     login = auth.sign_in_with_email_and_password(email, password)
#
#     # cred = credentials.Certificate('firebase-sdk.json')
#     # firebase_admin.initialize_app(cred)
#
#     db = firestore.client()
#     userid = ''
#     if 'Fisk.Edu' in facultysignin.email:
#         for i in facultysignin.email:
#             if i != '@':
#                 userid = userid + i
#             elif i == '@':
#                 break
#     # print(userid)
#
#     result = db.collection('FacultyandStaff').document(str(userid)).get()
#     result = result.to_dict()
#     first_name = result.get("First Name")
#     first_name = first_name.lower()
#     facultysignin.first_name = first_name.title()
#     last_name = result.get("Last Name")
#     last_name = last_name.lower()
#     last_name = last_name.title()
#     facultysignin.last_name = last_name.title()
#     email = result.get("Email")
#     email = email.lower()
#     facultysignin.email = email.title()
#
#     return render_template('facultypage.html', firstname=facultysignin.first_name, lastname=facultysignin.last_name,
#                            fiskemail=facultysignin.email), dict(userid=userid)
#
#     facultysignin()
#
# #
# @app.route('/retrievedata')
# def facultyretrievedata():
#     return render_template("dataoptions.html")
#     facultyretrievedata()
#
#
# @app.route('/group_data')
# def groupretrievedata():
#     return render_template("groupstudentchecker.html")
#     groupretrievedata()
#
#
# @app.route('/groupstudentchecker', methods=['POST', 'GET'])  # name of form
# def groupdatareport():
#     year = request.form['YEAR']
#     semester = request.form['SEMESTER']
#     Opportunity =  request.form['OPPORTUNITY']
#     return render_template('results.html')
#     groupdatareport()
#
#
# @app.route('/groupstudentchecker', methods=['POST', 'GET'])  # name of form
# def groupdatareport():
#     db = firestore.client()
#     usernames = []
#     year = request.form['YEAR']
#     semester = request.form['SEMESTER']
#     Opportunity =  request.form['OPPORTUNITY']
#     docs = db.collection('student').get()
#     return render_template(usernames=usernames)
#     groupdatareport()
#
# # def groupdatareport2():
# #     db = firestore.client()
# #     usernames = []
# #     year = groupdatareport.year
# #     semester = groupdatareport.semester
# #     Opportunity = groupdatareport.Opportunity
# #     docs = db.collection('student').get()
# #     if Opportunity == "Undergraduate: Internship Opportunity" and semester == "Winter":
# #         for doc in docs:
# #             doc = doc.to_dict()
# #             email = doc['Email']
# #             # print(email)
# #             if 'My.Fisk.Edu' in email:
# #                 userid = ''
# #                 for i in email:
# #                     if i != '@':
# #                         userid = userid + i
# #                     elif i == '@':
# #                         break
# #             usernames.append(userid)
# #
# #             table = [['Student Username', 'First Name', 'Last Name', 'Fisk Email', 'Classification', 'Internship Year',
# #                       'Company Name', 'Position', 'Hourly Pay']]
# #             for user in usernames:
# #                 doc_ref = db.collection('student').document(str(user))
# #                 docs = doc_ref.collection(str(year)).document("Winter Internship Information").get()
# #                 docs = docs.to_dict()
# #                 result = db.collection('student').document(str(user)).get()
# #                 result = result.to_dict()
# #                 first_name = result.get('First Name')
# #                 first_name = first_name.lower()
# #                 first_name = first_name.title()
# #                 last_name = result.get('Last Name')
# #                 last_name = last_name.lower()
# #                 last_name = last_name.title()
# #                 fisk_email = result.get('Email')
# #                 # print(fisk_email)
# #                 newlist = []
# #                 if docs:
# #                     order = {}
# #                     list = []
# #                     newlist = []
# #                     order = [0, 6, 2, 5, 8, 3, 7, 1, 4]
# #                     dict = {'Student Username': user, 'First Name': first_name, 'Last Name': last_name,
# #                             'Fisk Email': fisk_email}
# #                     dict.update(docs)
# #                     for key in dict.items():
# #                         list.append(key)
# #                         list.sort(reverse=True)
# #                     # print(list)
# #                     list = [list[i] for i in order]
# #
# #                     for i in list:
# #                         newlist.append(i[1])
# #                     table.append(newlist)
# #             # print(headers)
# #             finaltable = tabulate(table, tablefmt="html")
# #             # return('table.html')
# #             with open('templates/table.html', 'w') as f:
# #                 f.write(tabulate(table, tablefmt="html"))
# #             with open('templates/table.html', 'r') as infile, open(
# #                     '/Users/kehindeadekoya/PycharmProjects/ocpdhub/templates/groupstudentresultspage.html',
# #                     'r') as infile2, open(
# #                 'templates/studentgroupdatareport.html', 'w') as outfile:
# #                 for line in infile2:
# #                     outfile.write(line)
# #                 for line in infile:
# #                     outfile.write(line)
# #
# #     if Opportunity == "Undergraduate: Internship Opportunity" and semester == "Spring":
# #         for doc in docs:
# #             doc = doc.to_dict()
# #             email = doc['Email']
# #             # print(email)
# #             if 'My.Fisk.Edu' in email:
# #                 userid = ''
# #                 for i in email:
# #                     if i != '@':
# #                         userid = userid + i
# #                     elif i == '@':
# #                         break
# #             usernames.append(userid)
# #
# #             table = [['Student Username', 'First Name', 'Last Name', 'Fisk Email', 'Classification', 'Internship Year',
# #                       'Company Name', 'Position', 'Hourly Pay']]
# #             for user in usernames:
# #                 doc_ref = db.collection('student').document(str(user))
# #                 docs = doc_ref.collection(str(year)).document("Spring Internship Information").get()
# #                 docs = docs.to_dict()
# #                 result = db.collection('student').document(str(user)).get()
# #                 result = result.to_dict()
# #                 first_name = result.get('First Name')
# #                 first_name = first_name.lower()
# #                 first_name = first_name.title()
# #                 last_name = result.get('Last Name')
# #                 last_name = last_name.lower()
# #                 last_name = last_name.title()
# #                 fisk_email = result.get('Email')
# #                 # print(fisk_email)
# #                 newlist = []
# #                 if docs:
# #                     order = {}
# #                     list = []
# #                     newlist = []
# #                     order = [0, 6, 2, 5, 8, 3, 7, 1, 4]
# #                     dict = {'Student Username': user, 'First Name': first_name, 'Last Name': last_name,
# #                             'Fisk Email': fisk_email}
# #                     dict.update(docs)
# #                     for key in dict.items():
# #                         list.append(key)
# #                         list.sort(reverse=True)
# #                     # print(list)
# #                     list = [list[i] for i in order]
# #
# #                     for i in list:
# #                         newlist.append(i[1])
# #                     table.append(newlist)
# #             # print(headers)
# #             finaltable = tabulate(table, tablefmt="html")
# #             # return('table.html')
# #             with open('templates/table.html', 'w') as f:
# #                 f.write(tabulate(table, tablefmt="html"))
# #             with open('templates/table.html', 'r') as infile, open(
# #                     '/Users/kehindeadekoya/PycharmProjects/ocpdhub/templates/groupstudentresultspage.html',
# #                     'r') as infile2, open(
# #                 'templates/studentgroupdatareport.html', 'w') as outfile:
# #                 for line in infile2:
# #                     outfile.write(line)
# #                 for line in infile:
# #                     outfile.write(line)
# #
# #     if Opportunity == "Undergraduate: Internship Opportunity" and semester == "Summer":
# #         for doc in docs:
# #             doc = doc.to_dict()
# #             email = doc['Email']
# #             # print(email)
# #             if 'My.Fisk.Edu' in email:
# #                 userid = ''
# #                 for i in email:
# #                     if i != '@':
# #                         userid = userid + i
# #                     elif i == '@':
# #                         break
# #             usernames.append(userid)
# #
# #             table = [['Student Username', 'First Name', 'Last Name', 'Fisk Email', 'Classification', 'Internship Year',
# #                       'Company Name', 'Position', 'Hourly Pay']]
# #             for user in usernames:
# #                 doc_ref = db.collection('student').document(str(user))
# #                 docs = doc_ref.collection(str(year)).document("Summer Internship Information").get()
# #                 docs = docs.to_dict()
# #                 result = db.collection('student').document(str(user)).get()
# #                 result = result.to_dict()
# #                 first_name = result.get('First Name')
# #                 first_name = first_name.lower()
# #                 first_name = first_name.title()
# #                 last_name = result.get('Last Name')
# #                 last_name = last_name.lower()
# #                 last_name = last_name.title()
# #                 fisk_email = result.get('Email')
# #                 # print(fisk_email)
# #                 newlist = []
# #                 if docs:
# #                     order = {}
# #                     list = []
# #                     newlist = []
# #                     order = [0, 6, 2, 5, 8, 3, 7, 1, 4]
# #                     dict = {'Student Username': user, 'First Name': first_name, 'Last Name': last_name,
# #                             'Fisk Email': fisk_email}
# #                     dict.update(docs)
# #                     for key in dict.items():
# #                         list.append(key)
# #                         list.sort(reverse=True)
# #                     # print(list)
# #                     list = [list[i] for i in order]
# #
# #                     for i in list:
# #                         newlist.append(i[1])
# #                     table.append(newlist)
# #             # print(headers)
# #             finaltable = tabulate(table, tablefmt="html")
# #             # return('table.html')
# #             with open('templates/table.html', 'w') as f:
# #                 f.write(tabulate(table, tablefmt="html"))
# #             with open('templates/table.html', 'r') as infile, open(
# #                     '/Users/kehindeadekoya/PycharmProjects/ocpdhub/templates/groupstudentresultspage.html',
# #                     'r') as infile2, open(
# #                 'templates/studentgroupdatareport.html', 'w') as outfile:
# #                 for line in infile2:
# #                     outfile.write(line)
# #                 for line in infile:
# #                     outfile.write(line)
# #
# #     if Opportunity == "Undergraduate: Internship Opportunity" and semester == "Fall":
# #         for doc in docs:
# #             doc = doc.to_dict()
# #             email = doc['Email']
# #             # print(email)
# #             if 'My.Fisk.Edu' in email:
# #                 userid = ''
# #                 for i in email:
# #                     if i != '@':
# #                         userid = userid + i
# #                     elif i == '@':
# #                         break
# #             usernames.append(userid)
# #
# #             table = [['Student Username', 'First Name', 'Last Name', 'Fisk Email', 'Classification', 'Internship Year',
# #                       'Company Name', 'Position', 'Hourly Pay']]
# #             for user in usernames:
# #                 doc_ref = db.collection('student').document(str(user))
# #                 docs = doc_ref.collection(str(year)).document("Fall Internship Information").get()
# #                 docs = docs.to_dict()
# #                 result = db.collection('student').document(str(user)).get()
# #                 result = result.to_dict()
# #                 first_name = result.get('First Name')
# #                 first_name = first_name.lower()
# #                 first_name = first_name.title()
# #                 last_name = result.get('Last Name')
# #                 last_name = last_name.lower()
# #                 last_name = last_name.title()
# #                 fisk_email = result.get('Email')
# #                 # print(fisk_email)
# #                 newlist = []
# #                 if docs:
# #                     order = {}
# #                     list = []
# #                     newlist = []
# #                     order = [0, 6, 2, 5, 8, 3, 7, 1, 4]
# #                     dict = {'Student Username': user, 'First Name': first_name, 'Last Name': last_name,
# #                             'Fisk Email': fisk_email}
# #                     dict.update(docs)
# #                     for key in dict.items():
# #                         list.append(key)
# #                         list.sort(reverse=True)
# #                     # print(list)
# #                     list = [list[i] for i in order]
# #
# #                     for i in list:
# #                         newlist.append(i[1])
# #                     table.append(newlist)
# #             # print(headers)
# #             finaltable = tabulate(table, tablefmt="html")
# #             # return('table.html')
# #             # if finaltable != "":
# #             with open('templates/table.html', 'w') as f:
# #                 f.write(tabulate(table, tablefmt="html"))
# #             with open('templates/table.html', 'r') as infile, open(
# #                     '/Users/kehindeadekoya/PycharmProjects/ocpdhub/templates/groupstudentresultspage.html',
# #                     'r') as infile2, open(
# #                 'templates/studentgroupdatareport.html', 'w') as outfile:
# #                 for line in infile2:
# #                     outfile.write(line)
# #                 for line in infile:
# #                     outfile.write(line)
# # groupdatareport2()
#
# # @app.route('/reportlink')
# @app.route('/reportlink')  # name of form
# def studentgroupdatareport3():
#     return render_template('studentgroupdatareport.html')
#
db = firestore.client()

usernames = []
docs = db.collection('student').get()
year = "2022"
semester = "Fall"
oppurtunity = "Post Graduate: Graduate School Opportunity"
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
        table = [['Student Username', 'First Name', 'Last Name', 'Fisk Email', 'Personal Email', 'Year', 'University Name', 'Program Name', 'Degree']]
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
                order = [1,7,4,6,3,0,5,4,8]
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

    # # print(table[1])
    # for t in table:
    #     print(table[t][count])
    #     count=count +1
    # finaltable = tabulate(table, tablefmt="simple")
# docs = db.collection('student').where("Major", "==", "Mis").get()

# if Opportunity == "Undergraduate: Internship Opportunity" and semester == "Winter":
#     for doc in docs:
#         doc = doc.to_dict()
#         email = doc['Email']
#         # print(email)
#         if 'My.Fisk.Edu' in email:
#             userid = ''
#             for i in email:
#                 if i != '@':
#                     userid = userid + i
#                 elif i == '@':
#                     break
#         usernames.append(userid)
#
#         table = [['Student Username', 'First Name', 'Last Name', 'Fisk Email', 'Classification', 'Internship Year',
#                   'Company Name', 'Position', 'Hourly Pay']]
#         for user in usernames:
#             doc_ref = db.collection('student').document(str(user))
#             docs = doc_ref.collection(str(year)).document("Winter Internship Information").get()
#             docs = docs.to_dict()
#             result = db.collection('student').document(str(user)).get()
#             result = result.to_dict()
#             first_name = result.get('First Name')
#             first_name = first_name.lower()
#             first_name = first_name.title()
#             last_name = result.get('Last Name')
#             last_name = last_name.lower()
#             last_name = last_name.title()
#             fisk_email = result.get('Email')
#             # print(fisk_email)
#             newlist = []
#             if docs:
#                 order = {}
#                 list = []
#                 newlist = []
#                 order = [0, 6, 2, 5, 8, 3, 7, 1, 4]
#                 dict = {'Student Username': user, 'First Name': first_name, 'Last Name': last_name,
#                         'Fisk Email': fisk_email}
#                 dict.update(docs)
#                 for key in dict.items():
#                     list.append(key)
#                     list.sort(reverse=True)
#                 # print(list)
#                 list = [list[i] for i in order]
#
#                 for i in list:
#                     newlist.append(i[1])
#                 table.append(newlist)
#         # print(headers)
#         finaltable = tabulate(table, tablefmt="simple_grid")
#         # print(finaltable)
#     # render_template('studentgroupdatareport.html', finaltable=finaltable)
#     # render_template('studentgroupdatareport.html', finaltable=finaltable)
#     # return('table.html')
#     # with open('templates/table.html', 'w') as f:
#     #     f.write(tabulate(table, tablefmt="html"))
#     # with open('templates/table.html', 'r') as infile, open('/Users/kehindeadekoya/PycharmProjects/ocpdhub/templates/groupstudentresultspage.html', 'r') as infile2, open(
#     #         'templates/studentgroupdatareport.html', 'w') as outfile:
#     #     for line in infile2:
#     #         outfile.write(line)
#     #     for line in infile:
#     #         outfile.write(line)
#
# if Opportunity == "Undergraduate: Internship Opportunity" and semester == "Spring":
#     for doc in docs:
#         doc = doc.to_dict()
#         email = doc['Email']
#         # print(email)
#         if 'My.Fisk.Edu' in email:
#             userid = ''
#             for i in email:
#                 if i != '@':
#                     userid = userid + i
#                 elif i == '@':
#                     break
#         usernames.append(userid)
#
#         table = [['Student Username', 'First Name', 'Last Name', 'Fisk Email', 'Classification', 'Internship Year',
#                   'Company Name', 'Position', 'Hourly Pay']]
#         for user in usernames:
#             doc_ref = db.collection('student').document(str(user))
#             docs = doc_ref.collection(str(year)).document("Spring Internship Information").get()
#             docs = docs.to_dict()
#             result = db.collection('student').document(str(user)).get()
#             result = result.to_dict()
#             first_name = result.get('First Name')
#             first_name = first_name.lower()
#             first_name = first_name.title()
#             last_name = result.get('Last Name')
#             last_name = last_name.lower()
#             last_name = last_name.title()
#             fisk_email = result.get('Email')
#             # print(fisk_email)
#             newlist = []
#             if docs:
#                 order = {}
#                 list = []
#                 newlist = []
#                 order = [0, 6, 2, 5, 8, 3, 7, 1, 4]
#                 dict = {'Student Username': user, 'First Name': first_name, 'Last Name': last_name,
#                         'Fisk Email': fisk_email}
#                 dict.update(docs)
#                 for key in dict.items():
#                     list.append(key)
#                     list.sort(reverse=True)
#                 # print(list)
#                 list = [list[i] for i in order]
#
#                 for i in list:
#                     newlist.append(i[1])
#                 table.append(newlist)
#         # print(headers)
#         finaltable = tabulate(table, tablefmt="simple_grid")
#         # print(finaltable)
#         # render_template('studentgroupdatareport.html', finaltable=finaltable)
#         # return('table.html')
#         # with open('templates/table.html', 'w') as f:
#         #     f.write(tabulate(table, tablefmt="html"))
#         # with open('templates/table.html', 'r') as infile, open(
#         #         '/Users/kehindeadekoya/PycharmProjects/ocpdhub/templates/groupstudentresultspage.html',
#         #         'r') as infile2, open(
#         #         'templates/studentgroupdatareport.html', 'w') as outfile:
#         #     for line in infile2:
#         #         outfile.write(line)
#         #     for line in infile:
#         #         outfile.write(line)
#
# if Opportunity == "Undergraduate: Internship Opportunity" and semester == "Summer":
#     for doc in docs:
#         doc = doc.to_dict()
#         email = doc['Email']
#         # print(email)
#         if 'My.Fisk.Edu' in email:
#             userid = ''
#             for i in email:
#                 if i != '@':
#                     userid = userid + i
#                 elif i == '@':
#                     break
#         usernames.append(userid)
#
#         table = [['Student Username', 'First Name', 'Last Name', 'Fisk Email', 'Classification', 'Internship Year',
#                   'Company Name', 'Position', 'Hourly Pay']]
#         for user in usernames:
#             doc_ref = db.collection('student').document(str(user))
#             docs = doc_ref.collection(str(year)).document("Summer Internship Information").get()
#             docs = docs.to_dict()
#             result = db.collection('student').document(str(user)).get()
#             result = result.to_dict()
#             first_name = result.get('First Name')
#             first_name = first_name.lower()
#             first_name = first_name.title()
#             last_name = result.get('Last Name')
#             last_name = last_name.lower()
#             last_name = last_name.title()
#             fisk_email = result.get('Email')
#             # print(fisk_email)
#             newlist = []
#             if docs:
#                 order = {}
#                 list = []
#                 newlist = []
#                 order = [0, 6, 2, 5, 8, 3, 7, 1, 4]
#                 dict = {'Student Username': user, 'First Name': first_name, 'Last Name': last_name,
#                         'Fisk Email': fisk_email}
#                 dict.update(docs)
#                 for key in dict.items():
#                     list.append(key)
#                     list.sort(reverse=True)
#                 # print(list)
#                 list = [list[i] for i in order]
#
#                 for i in list:
#                     newlist.append(i[1])
#                 table.append(newlist)
#         # print(headers)
#     finaltable = tabulate(table, tablefmt="simple_grid")
#     # print(finaltable)
#     # return('table.html')
#     # with open('templates/table.html', 'w') as f:
#     #     f.write(tabulate(table, tablefmt="html"))
#     # with open('templates/table.html', 'r') as infile, open(
#     #         '/Users/kehindeadekoya/PycharmProjects/ocpdhub/templates/groupstudentresultspage.html',
#     #         'r') as infile2, open(
#     #     'templates/studentgroupdatareport.html', 'w') as outfile:
#     #     for line in infile2:
#     #         outfile.write(line)
#     #     for line in infile:
#     #         outfile.write(line)
#
# if Opportunity == "Undergraduate: Internship Opportunity" and semester == "Fall":
#     for doc in docs:
#         doc = doc.to_dict()
#         email = doc['Email']
#         # print(email)
#         if 'My.Fisk.Edu' in email:
#             userid = ''
#             for i in email:
#                 if i != '@':
#                     userid = userid + i
#                 elif i == '@':
#                     break
#         usernames.append(userid)
#
#         table = [['Student Username', 'First Name', 'Last Name', 'Fisk Email', 'Classification', 'Internship Year',
#                   'Company Name', 'Position', 'Hourly Pay']]
#         for user in usernames:
#             doc_ref = db.collection('student').document(str(user))
#             docs = doc_ref.collection(str(year)).document("Fall Internship Information").get()
#             docs = docs.to_dict()
#             result = db.collection('student').document(str(user)).get()
#             result = result.to_dict()
#             first_name = result.get('First Name')
#             first_name = first_name.lower()
#             first_name = first_name.title()
#             last_name = result.get('Last Name')
#             last_name = last_name.lower()
#             last_name = last_name.title()
#             fisk_email = result.get('Email')
#             # print(fisk_email)
#             newlist = []
#             if docs:
#                 order = {}
#                 list = []
#                 newlist = []
#                 order = [0, 6, 2, 5, 8, 3, 7, 1, 4]
#                 dict = {'Student Username': user, 'First Name': first_name, 'Last Name': last_name,
#                         'Fisk Email': fisk_email}
#                 dict.update(docs)
#                 for key in dict.items():
#                     list.append(key)
#                     list.sort(reverse=True)
#                 # print(list)
#                 list = [list[i] for i in order]
#
#                 for i in list:
#                     newlist.append(i[1])
#                 table.append(newlist)
#         # print(headers)
#         finaltable = tabulate(table, tablefmt="simple_grid")
# print(finaltable)

