
from flask import Flask, render_template, request, url_for


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
    "apiKey": "AIzaSyDuK0URbMlmFuJ1nXzWkqwgZhnBEQACeJ8",
    "authDomain": "fisk-ocpd-data-hub-afba1.firebaseapp.com",
    "projectId": "fisk-ocpd-data-hub-afba1",
    "storageBucket": "fisk-ocpd-data-hub-afba1.appspot.com",
    "messagingSenderId": "521026036958",
    "appId": "1:521026036958:web:da98df24f42369e428ce4f",
    "measurementId": "G-DHK5S1DP47"
}

app = Flask(__name__)
app.config['SERVER_NAME'] = 'localhost:5000'


# defining the url or route for the website
#@app.route('/fiskocpddatahub')
cred = credentials.Certificate('firebase-sdk.json')
firebase_admin.initialize_app(cred)



# creating a homepage for the dashboard
@app.route('/')
def homepage():
    return render_template("website.html")  # returns/runs the code from the html file


# student info

# student login
@app.route('/student')
def studentlogin():
    return render_template("student.html")


@app.route('/')
def my_form():
    return render_template('student.html')


@app.route('/newstudent', methods=['POST', 'GET'])  # name of form
def studentsignin():
    firebase = pyrebase.initialize_app(firebaseConfig)
    auth = firebase.auth()
    email = request.form['EMAIL']
    email = email.lower()
    studentsignin.email = email.title()
    password = request.form['PASSWORD']
    login = auth.sign_in_with_email_and_password(email, password)

    # cred = credentials.Certificate('firebase-sdk.json')
    # firebase_admin.initialize_app(cred)

    db = firestore.client()
    userid = ''
    if 'My.Fisk.Edu' in studentsignin.email:
        for i in studentsignin.email:
            if i != '@':
                userid = userid + i
            elif i == '@':
                break
    # print(userid)

    result = db.collection('student').document(str(userid)).get()
    result = result.to_dict()
    first_name = result.get("First Name")
    first_name = first_name.lower()
    studentsignin.first_name = first_name.title()
    last_name = result.get("Last Name")
    last_name = last_name.lower()
    last_name = last_name.title()
    studentsignin.last_name = last_name.title()
    email = result.get("Email")
    email = email.lower()
    studentsignin.email = email.title()
    student_number = result.get("Student Number")
    student_number = student_number.lower()
    studentsignin.student_number = student_number.title()
    major = result.get("Major")
    major = major.lower()
    studentsignin.major = major.title()

    return render_template('studentpage.html', firstname=studentsignin.first_name, lastname=studentsignin.last_name,
                           fiskemail=studentsignin.email, studentNumber=studentsignin.student_number,
                           fiskmajor=studentsignin.major), dict(userid=userid)

    studentsignin()


# student sign up
@app.route('/StudentSignupsheet')
def studentSignUp():
    return render_template("StudentSignUp.html")


@app.route('/')
def my_form2():
    return render_template('student.html')


@app.route('/newstudentsignup', methods=['POST', 'GET'])  # name of form
def studentsignup():
    # cred = credentials.Certificate('firebase-sdk.json')
    # firebase_admin.initialize_app(cred)
    first_name = request.form['FIRSTNAME']
    first_name = first_name.lower()
    studentsignup.first_name = first_name.title()
    last_name = request.form['LASTNAME']
    last_name = last_name.lower()
    studentsignup.last_name = last_name.title()
    email = request.form['EMAIL']
    email = email.lower()
    studentsignup.email = email.title()
    password = request.form['PASSWORD']
    major = request.form['MAJOR']
    major = major.lower()
    studentsignup.major = major.title()
    student_number = request.form['STUDENTIDNUMBER']
    student_number = student_number.lower()
    studentsignup.student_number = student_number.title()

    userid = ''
    if 'My.Fisk.Edu' in studentsignup.email:
        for i in studentsignup.email:
            if i != '@':
                userid = userid + i
            elif i == '@':
                break
    # print(userid)
    user = auth.create_user(uid=userid, email=studentsignup.email, password=password)

    db = firestore.client()

    doc_ref = db.collection('student').document(str(userid))

    doc_ref.set({
        'UserID': str(userid),
        'First Name': str(first_name),
        'Last Name': str(last_name),
        'Email': str(studentsignup.email),
        'Student Number': str(student_number),
        'Major': str(studentsignup.major)
    })
    return render_template('student.html', firstname=studentsignup.first_name, lastname=studentsignup.last_name,
                           fiskemail=studentsignup.email, studentNumber=studentsignup.student_number,
                           fiskmajor=studentsignup.major)
    studentsignup()


@app.route('/student-passwordreset')
def studentreset1():
    firebase = pyrebase.initialize_app(firebaseConfig)
    auth = firebase.auth()
    return render_template('passwordreset.html')


@app.route('/passwordreset', methods=['POST', 'GET'])  # name of form
def studentreset2():
    # cred = credentials.Certificate('firebase-sdk.json')
    # firebase_admin.initialize_app(cred)
    # password reset
    email = request.form['EMAIL']
    email = email.lower()
    email = email.title()
    link = auth.generate_password_reset_link(email, action_code_settings=None)
    return redirect(str(link), code=302)


# faculty info
# faculty login
@app.route('/faculty')
def facultylogin():
    return render_template("faculty.html")


@app.route('/staff')
def stafflogin():
    return render_template("faculty.html")


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


# faculty sign up
@app.route('/Facultysignupsheet')
def facultySignUp():
    return render_template("FacultySignUp.html")


@app.route('/')
def my_form4():
    return render_template('faculty.html')


@app.route('/newfaculysignup', methods=['POST', 'GET'])  # name of form
def facultysignup():
    # cred = credentials.Certificate('firebase-sdk.json')
    # firebase_admin.initialize_app(cred)
    first_name = request.form['FIRSTNAME']
    first_name = first_name.lower()
    first_name = first_name.title()
    last_name = request.form['LASTNAME']
    last_name = last_name.lower()
    last_name = last_name.title()
    email = request.form['EMAIL']
    email = email.lower()
    email = email.title()
    password = request.form['PASSWORD']

    userid = ''
    if 'Fisk.Edu' in email:
        for i in email:
            if i != '@':
                userid = userid + i
            elif i == '@':
                break

    # print(id)
    user = auth.create_user(uid=userid, email=email, password=password)

    db = firestore.client()

    doc_ref = db.collection('FacultyandStaff').document(str(userid))

    doc_ref.set({
        'UserID': str(userid),
        'First Name': str(first_name),
        'Last Name': str(last_name),
        'Email': str(email)
    })
    return render_template('faculty.html', firstname=first_name, lastname=last_name, fiskemail=email)
    facultysignup()


# password reset
@app.route('/faculy-passwordreset')
def facultyreset1():
    firebase = pyrebase.initialize_app(firebaseConfig)
    auth = firebase.auth()
    return render_template('passwordreset.html')


@app.route('/passwordreset', methods=['POST', 'GET'])  # name of form
def facultyreset2():
    # cred = credentials.Certificate('firebase-sdk.json')
    # firebase_admin.initialize_app(cred)
    # password reset
    email = request.form['EMAIL']
    email = email.lower()
    email = email.title()
    link = auth.generate_password_reset_link(email, action_code_settings=None)
    return redirect(str(link), code=302)


# fall semester
@app.route('/fall_survey')
def fallbutton():
    # cred = credentials.Certificate('firebase-sdk.json')
    # firebase_admin.initialize_app(cred)
    db = firestore.client()
    userid = ''
    if 'My.Fisk.Edu' in studentsignin.email:
        for i in studentsignin.email:
            if i != '@':
                userid = userid + i
            elif i == '@':
                break
    doc_ref = db.collection('student').document(str(userid))
    docs = doc_ref.collection(str('2022')).get()
    docs = doc_ref.collection(str('2022')).document('Fall Internship Information').get()
    print(docs.to_dict())
    info_doc = docs.to_dict()
    if info_doc:
        grade = info_doc['Classification']
        year = info_doc['Internship Year']
        company_name = info_doc['Company Name']
        pay = info_doc['Hourly Pay']
        position = info_doc['Position']
    else:
        grade = ""
        year = ""
        company_name = ""
        pay = ""
        position = ""

    return render_template("fallinternshipfollowup.html", grade=grade.title(), year=year, company_name=company_name,
                           pay=pay, position=position.title())
    fallbutton()


@app.route('/fall_internship_info')
def fallbuttonpt2():
    # cred = credentials.Certificate('firebase-sdk.json')
    # firebase_admin.initialize_app(cred)
    db = firestore.client()
    userid = ''
    if 'My.Fisk.Edu' in studentsignin.email:
        for i in studentsignin.email:
            if i != '@':
                userid = userid + i
            elif i == '@':
                break
    doc_ref = db.collection('student').document(str(userid))
    docs = doc_ref.collection(str('2022')).get()
    docs = doc_ref.collection(str('2022')).document('Fall Internship Information').get()
    print(docs.to_dict())
    info_doc = docs.to_dict()
    if info_doc:
        grade = info_doc['Classification']
        year = info_doc['Internship Year']
        company_name = info_doc['Company Name']
        pay = info_doc['Hourly Pay']
        position = info_doc['Position']
    else:
        grade = ""
        year = ""
        company_name = ""
        pay = ""
        position = ""

    return render_template("FallForm.html", grade=grade.title(), year=year, company_name=company_name, pay=pay,
                           position=position.title())
    fallbuttonpt2()


@app.route('/')
def fall_form():
    return render_template('FallForm.html')


@app.route('/fallsurvey', methods=['POST', 'GET'])  # name of form
def fall_survey():
    # cred = credentials.Certificate('firebase-sdk.json')
    # firebase_admin.initialize_app(cred)

    email = studentsignin.email
    # email = request.form['EMAIL']
    email = email.lower()
    email = email.title()
    id = ''
    if 'My.Fisk.Edu' in email:
        for i in email:
            if i != '@':
                id = id + i
            elif i == '@':
                break

    classification = request.form['CLASSIFICATION']
    year = request.form['YEAR']
    company_name = request.form['COMPANYNAME']
    position = request.form['POSITION']
    pay = request.form['PAY']

    db = firestore.client()
    doc_ref = db.collection('student').document(str(id))
    fall_info = doc_ref.collection(str(year)).document('Fall Internship Information')

    fall_info.set({
        'Classification': str(classification),
        'Internship Year': str(year),
        'Company Name': str(company_name),
        'Position': str(position),
        'Hourly Pay': str(pay)
    })

    # retrieving data
    return render_template('CompletedForm.html')
    fall_survey()


# spring semester
@app.route('/spring_survey')
def springbutton():
    # cred = credentials.Certificate('firebase-sdk.json')
    # firebase_admin.initialize_app(cred)
    db = firestore.client()
    userid = ''
    if 'My.Fisk.Edu' in studentsignin.email:
        for i in studentsignin.email:
            if i != '@':
                userid = userid + i
            elif i == '@':
                break
    doc_ref = db.collection('student').document(str(userid))
    docs = doc_ref.collection(str('2022')).get()
    docs = doc_ref.collection(str('2022')).document('Spring Internship Information').get()
    print(docs.to_dict())
    info_doc = docs.to_dict()
    if info_doc:
        grade = info_doc['Classification']
        year = info_doc['Internship Year']
        company_name = info_doc['Company Name']
        pay = info_doc['Hourly Pay']
        position = info_doc['Position']
    else:
        grade = ""
        year = ""
        company_name = ""
        pay = ""
        position = ""

    return render_template("springinternshipfollowup.html", grade=grade.title(), year=year, company_name=company_name,
                           pay=pay, position=position.title())
    springbutton()


@app.route('/spring_internship_info')
def springbuttonpt2():
    # cred = credentials.Certificate('firebase-sdk.json')
    # firebase_admin.initialize_app(cred)
    db = firestore.client()
    userid = ''
    if 'My.Fisk.Edu' in studentsignin.email:
        for i in studentsignin.email:
            if i != '@':
                userid = userid + i
            elif i == '@':
                break
    doc_ref = db.collection('student').document(str(userid))
    docs = doc_ref.collection(str('2022')).get()
    docs = doc_ref.collection(str('2022')).document('Spring Internship Information').get()
    print(docs.to_dict())
    info_doc = docs.to_dict()
    if info_doc:
        grade = info_doc['Classification']
        year = info_doc['Internship Year']
        company_name = info_doc['Company Name']
        pay = info_doc['Hourly Pay']
        position = info_doc['Position']
    else:
        grade = ""
        year = ""
        company_name = ""
        pay = ""
        position = ""

    # return render_template("Fa.html", grade=grade.title(), year=year, company_name=company_name,
    #                        pay=pay, position=position.title())
    return render_template("SpringForm.html", grade=grade.title(), year=year, company_name=company_name, pay=pay,
                           position=position.title())
    springbuttonpt2()


@app.route('/')
def spring_form():
    return render_template('SpringForm.html')


@app.route('/springsurvey', methods=['POST', 'GET'])  # name of form
def spring_survey():
    # cred = credentials.Certificate('firebase-sdk.json')
    # firebase_admin.initialize_app(cred)

    email = studentsignin.email
    # email = request.form['EMAIL']
    email = email.lower()
    email = email.title()
    id = ''
    if 'My.Fisk.Edu' in email:
        for i in email:
            if i != '@':
                id = id + i
            elif i == '@':
                break

    classification = request.form['CLASSIFICATION']
    year = request.form['YEAR']
    company_name = request.form['COMPANYNAME']
    position = request.form['POSITION']
    pay = request.form['PAY']

    db = firestore.client()
    doc_ref = db.collection('student').document(str(id))
    spring_info = doc_ref.collection(str(year)).document('Spring Internship Information')

    spring_info.set({
        'Classification': str(classification),
        'Internship Year': str(year),
        'Company Name': str(company_name),
        'Position': str(position),
        'Hourly Pay': str(pay)
    })

    # retrieving data

    return render_template('CompletedForm.html')
    spring_survey()


# summer semester
@app.route('/summer_survey')
def summerbutton():
    # cred = credentials.Certificate('firebase-sdk.json')
    # firebase_admin.initialize_app(cred)
    db = firestore.client()
    userid = ''
    if 'My.Fisk.Edu' in studentsignin.email:
        for i in studentsignin.email:
            if i != '@':
                userid = userid + i
            elif i == '@':
                break
    doc_ref = db.collection('student').document(str(userid))
    docs = doc_ref.collection(str('2022')).get()
    docs = doc_ref.collection(str('2022')).document('Summer Internship Information').get()
    print(docs.to_dict())
    info_doc = docs.to_dict()
    if info_doc:
        grade = info_doc['Classification']
        year = info_doc['Internship Year']
        company_name = info_doc['Company Name']
        pay = info_doc['Hourly Pay']
        position = info_doc['Position']
    else:
        grade = ""
        year = ""
        company_name = ""
        pay = ""
        position = ""

    return render_template("summerinternshipfollowup.html", grade=grade.title(), year=year, company_name=company_name,
                           pay=pay, position=position.title())
    summerbutton()


@app.route('/summer_internship_info')
def summerbuttonpt2():
    # cred = credentials.Certificate('firebase-sdk.json')
    # firebase_admin.initialize_app(cred)
    db = firestore.client()
    userid = ''
    if 'My.Fisk.Edu' in studentsignin.email:
        for i in studentsignin.email:
            if i != '@':
                userid = userid + i
            elif i == '@':
                break
    doc_ref = db.collection('student').document(str(userid))
    docs = doc_ref.collection(str('2022')).get()
    docs = doc_ref.collection(str('2022')).document('Summer Internship Information').get()
    print(docs.to_dict())
    info_doc = docs.to_dict()
    if info_doc:
        grade = info_doc['Classification']
        year = info_doc['Internship Year']
        company_name = info_doc['Company Name']
        pay = info_doc['Hourly Pay']
        position = info_doc['Position']
    else:
        grade = ""
        year = ""
        company_name = ""
        pay = ""
        position = ""

    # return render_template("Fa.html", grade=grade.title(), year=year, company_name=company_name,
    #                        pay=pay, position=position.title())
    return render_template("SummerForm.html", grade=grade.title(), year=year, company_name=company_name, pay=pay,
                           position=position.title())
    summerbuttonpt2()


@app.route('/')
def summer_form():
    return render_template('SummerForm.html')


@app.route('/summersurvey', methods=['POST', 'GET'])  # name of form
def summer_survey():
    # cred = credentials.Certificate('firebase-sdk.json')
    # firebase_admin.initialize_app(cred)

    email = studentsignin.email
    # email = request.form['EMAIL']
    email = email.lower()
    email = email.title()
    id = ''
    if 'My.Fisk.Edu' in email:
        for i in email:
            if i != '@':
                id = id + i
            elif i == '@':
                break

    classification = request.form['CLASSIFICATION']
    year = request.form['YEAR']
    company_name = request.form['COMPANYNAME']
    position = request.form['POSITION']
    pay = request.form['PAY']

    db = firestore.client()
    doc_ref = db.collection('student').document(str(id))
    summer_info = doc_ref.collection(str(year)).document('Summer Internship Information')

    summer_info.set({
        'Classification': str(classification),
        'Internship Year': str(year),
        'Company Name': str(company_name),
        'Position': str(position),
        'Hourly Pay': str(pay)
    })

    # retrieving data

    return render_template('CompletedForm.html')
    summer_survey()


# winter semester
@app.route('/winter_survey')
def winterbutton():
    # cred = credentials.Certificate('firebase-sdk.json')
    # firebase_admin.initialize_app(cred)
    db = firestore.client()
    userid = ''
    if 'My.Fisk.Edu' in studentsignin.email:
        for i in studentsignin.email:
            if i != '@':
                userid = userid + i
            elif i == '@':
                break
    doc_ref = db.collection('student').document(str(userid))
    docs = doc_ref.collection(str('2022')).get()
    docs = doc_ref.collection(str('2022')).document('Winter Internship Information').get()
    print(docs.to_dict())
    info_doc = docs.to_dict()
    if info_doc:
        grade = info_doc['Classification']
        year = info_doc['Internship Year']
        company_name = info_doc['Company Name']
        pay = info_doc['Hourly Pay']
        position = info_doc['Position']
    else:
        grade = ""
        year = ""
        company_name = ""
        pay = ""
        position = ""

    return render_template("winterinternshipfollowup.html", grade=grade.title(), year=year, company_name=company_name,
                           pay=pay, position=position.title())
    winterbutton()


@app.route('/winter_internship_info')
def winterbuttonpt2():
    # cred = credentials.Certificate('firebase-sdk.json')
    # firebase_admin.initialize_app(cred)
    db = firestore.client()
    userid = ''
    if 'My.Fisk.Edu' in studentsignin.email:
        for i in studentsignin.email:
            if i != '@':
                userid = userid + i
            elif i == '@':
                break
    doc_ref = db.collection('student').document(str(userid))
    docs = doc_ref.collection(str('2022')).get()
    docs = doc_ref.collection(str('2022')).document('Winter Internship Information').get()
    print(docs.to_dict())
    info_doc = docs.to_dict()
    if info_doc:
        grade = info_doc['Classification']
        year = info_doc['Internship Year']
        company_name = info_doc['Company Name']
        pay = info_doc['Hourly Pay']
        position = info_doc['Position']
    else:
        grade = ""
        year = ""
        company_name = ""
        pay = ""
        position = ""

    # return render_template("Fa.html", grade=grade.title(), year=year, company_name=company_name,
    #                        pay=pay, position=position.title())
    return render_template("WinterForm.html", grade=grade.title(), year=year, company_name=company_name, pay=pay,
                           position=position.title())
    winterbuttonpt2()


@app.route('/')
def winter_form():
    return render_template('WinterForm.html')


@app.route('/wintersurvey', methods=['POST', 'GET'])  # name of form
def winter_survey():
    # cred = credentials.Certificate('firebase-sdk.json')
    # firebase_admin.initialize_app(cred)

    email = studentsignin.email
    # email = request.form['EMAIL']
    email = email.lower()
    email = email.title()
    id = ''
    if 'My.Fisk.Edu' in email:
        for i in email:
            if i != '@':
                id = id + i
            elif i == '@':
                break

    classification = request.form['CLASSIFICATION']
    year = request.form['YEAR']
    company_name = request.form['COMPANYNAME']
    position = request.form['POSITION']
    pay = request.form['PAY']

    db = firestore.client()
    doc_ref = db.collection('student').document(str(id))
    winter_info = doc_ref.collection(str(year)).document('Winter Internship Information')

    winter_info.set({
        'Classification': str(classification),
        'Internship Year': str(year),
        'Company Name': str(company_name),
        'Position': str(position),
        'Hourly Pay': str(pay)
    })

    # retrieving data

    return render_template('CompletedForm.html')
    winter_survey()


@app.route('/fallresearch_survey')
def fallresearchbutton():
    # cred = credentials.Certificate('firebase-sdk.json')
    # firebase_admin.initialize_app(cred)
    db = firestore.client()
    userid = ''
    if 'My.Fisk.Edu' in studentsignin.email:
        for i in studentsignin.email:
            if i != '@':
                userid = userid + i
            elif i == '@':
                break
    doc_ref = db.collection('student').document(str(userid))
    docs = doc_ref.collection(str('2022')).get()
    docs = doc_ref.collection(str('2022')).document('Fall Research Experience Information').get()
    print(docs.to_dict())
    info_doc = docs.to_dict()

    if info_doc:
        classification = info_doc['Classification']
        year = info_doc['Year']
        uni_name = info_doc['University Name']
        program = info_doc['Program Name']
        topic = info_doc['Topic']
        conference = info_doc['Conference']
        pay = info_doc['Pay']
    else:
        classification = ""
        year = ""
        uni_name = ""
        program = ""
        topic = ""
        conference = ""
        pay = ""

    # return render_template("Fa.html", grade=grade.title(), year=year, company_name=company_name,
    #                        pay=pay, position=position.title())
    return render_template("fallresearchForm.html", topic=topic, uni_name=uni_name, program=program,
                           conference=conference.title(), pay=pay, year=year, classification=classification)
    fallresearchbutton()


# return render_template("FallForm.html", grade=grade.title(), year = year, company_name = company_name, pay = pay, position = position.title())
# fallbutton()

@app.route('/fallresearchsurvey', methods=['POST', 'GET'])  # name of form
def fallresearch_survey():
    # cred = credentials.Certificate('firebase-sdk.json')
    # firebase_admin.initialize_app(cred)
    email = studentsignin.email
    # email = request.form['EMAIL']
    email = email.lower()
    email = email.title()
    id = ''
    if 'My.Fisk.Edu' in email:
        for i in email:
            if i != '@':
                id = id + i
            elif i == '@':
                break

    db = firestore.client()
    doc_ref = db.collection('student').document(str(id))
    research_info = doc_ref.collection('2022').document('Fall Research Experience Information')

    classification = request.form['CLASSIFICATION']
    uni_name = request.form['UNINAME']
    year = request.form['YEAR']
    conference = request.form['CONFERENCE']
    program = request.form['PROGRAM']
    pay = request.form['PAY']
    topic = request.form['TOPIC']

    research_info.set({
        'Fisk Email': str(email),
        'Classification': str(classification),
        'Year': str(year),
        'University Name': str(uni_name),
        'Program Name': str(program),
        'Topic': str(topic),
        'Conference': str(conference),
        'Pay': str(pay)
    })
    return render_template('Completedform.html')
    fallresearch_survey()


@app.route('/springresearch_survey')
def springresearchbutton():
    # cred = credentials.Certificate('firebase-sdk.json')
    # firebase_admin.initialize_app(cred)
    db = firestore.client()
    userid = ''
    if 'My.Fisk.Edu' in studentsignin.email:
        for i in studentsignin.email:
            if i != '@':
                userid = userid + i
            elif i == '@':
                break
    doc_ref = db.collection('student').document(str(userid))
    docs = doc_ref.collection(str('2022')).get()
    docs = doc_ref.collection(str('2022')).document('Spring Research Experience Information').get()
    print(docs.to_dict())
    info_doc = docs.to_dict()

    if info_doc:
        classification = info_doc['Classification']
        year = info_doc['Year']
        uni_name = info_doc['University Name']
        program = info_doc['Program Name']
        topic = info_doc['Topic']
        conference = info_doc['Conference']
        pay = info_doc['Pay']
    else:
        classification = ""
        year = ""
        uni_name = ""
        program = ""
        topic = ""
        conference = ""
        pay = ""

    # return render_template("Fa.html", grade=grade.title(), year=year, company_name=company_name,
    #                        pay=pay, position=position.title())
    return render_template("springresearchForm.html", topic=topic, uni_name=uni_name, program=program,
                           conference=conference.title(), pay=pay, year=year, classification=classification)
    springresearchbutton()


# return render_template("FallForm.html", grade=grade.title(), year = year, company_name = company_name, pay = pay, position = position.title())
# fallbutton()

@app.route('/springresearchsurvey', methods=['POST', 'GET'])  # name of form
def springresearch_survey():
    # cred = credentials.Certificate('firebase-sdk.json')
    # firebase_admin.initialize_app(cred)
    email = studentsignin.email
    # email = request.form['EMAIL']
    email = email.lower()
    email = email.title()
    id = ''
    if 'My.Fisk.Edu' in email:
        for i in email:
            if i != '@':
                id = id + i
            elif i == '@':
                break

    db = firestore.client()
    doc_ref = db.collection('student').document(str(id))
    research_info = doc_ref.collection('2022').document('Spring Research Experience Information')

    classification = request.form['CLASSIFICATION']
    uni_name = request.form['UNINAME']
    year = request.form['YEAR']
    conference = request.form['CONFERENCE']
    program = request.form['PROGRAM']
    pay = request.form['PAY']
    topic = request.form['TOPIC']

    research_info.set({
        'Fisk Email': str(email),
        'Year': str(year),
        'Classification': str(classification),
        'University Name': str(uni_name),
        'Program Name': str(program),
        'Topic': str(topic),
        'Conference': str(conference),
        'Pay': str(pay)
    })
    return render_template('Completedform.html')
    springresearch_survey()


@app.route('/summerresearch_survey')
def summerresearchbutton():
    # cred = credentials.Certificate('firebase-sdk.json')
    # firebase_admin.initialize_app(cred)
    db = firestore.client()
    userid = ''
    if 'My.Fisk.Edu' in studentsignin.email:
        for i in studentsignin.email:
            if i != '@':
                userid = userid + i
            elif i == '@':
                break
    doc_ref = db.collection('student').document(str(userid))
    docs = doc_ref.collection(str('2022')).get()
    docs = doc_ref.collection(str('2022')).document('Summer Research Experience Information').get()
    print(docs.to_dict())
    info_doc = docs.to_dict()

    if info_doc:
        classification = info_doc['Classification']
        year = info_doc['Year']
        uni_name = info_doc['University Name']
        program = info_doc['Program Name']
        topic = info_doc['Topic']
        conference = info_doc['Conference']
        pay = info_doc['Pay']
    else:
        classification = ""
        year = ""
        uni_name = ""
        program = ""
        topic = ""
        conference = ""
        pay = ""

    # return render_template("Fa.html", grade=grade.title(), year=year, company_name=company_name,
    #                        pay=pay, position=position.title())
    return render_template("summerresearchForm.html", topic=topic, uni_name=uni_name, program=program,
                           conference=conference.title(), pay=pay, year=year, classification=classification)
    summerresearchbutton()


# return render_template("FallForm.html", grade=grade.title(), year = year, company_name = company_name, pay = pay, position = position.title())
# fallbutton()

@app.route('/summerresearchsurvey', methods=['POST', 'GET'])  # name of form
def summerresearch_survey():
    # cred = credentials.Certificate('firebase-sdk.json')
    # firebase_admin.initialize_app(cred)
    email = studentsignin.email
    # email = request.form['EMAIL']
    email = email.lower()
    email = email.title()
    id = ''
    if 'My.Fisk.Edu' in email:
        for i in email:
            if i != '@':
                id = id + i
            elif i == '@':
                break

    db = firestore.client()
    doc_ref = db.collection('student').document(str(id))
    research_info = doc_ref.collection('2022').document('Summer Research Experience Information')

    classification = request.form['CLASSIFICATION']
    uni_name = request.form['UNINAME']
    year = request.form['YEAR']
    conference = request.form['CONFERENCE']
    program = request.form['PROGRAM']
    pay = request.form['PAY']
    topic = request.form['TOPIC']

    research_info.set({
        'Fisk Email': str(email),
        'Year': str(year),
        'Classification': str(classification),
        'University Name': str(uni_name),
        'Program Name': str(program),
        'Topic': str(topic),
        'Conference': str(conference),
        'Pay': str(pay)
    })
    return render_template('Completedform.html')
    summerresearch_survey()


@app.route('/winterresearch_survey')
def winterresearchbutton():
    # cred = credentials.Certificate('firebase-sdk.json')
    # firebase_admin.initialize_app(cred)
    db = firestore.client()
    userid = ''
    if 'My.Fisk.Edu' in studentsignin.email:
        for i in studentsignin.email:
            if i != '@':
                userid = userid + i
            elif i == '@':
                break
    doc_ref = db.collection('student').document(str(userid))
    docs = doc_ref.collection(str('2022')).get()
    docs = doc_ref.collection(str('2022')).document('Winter Research Experience Information').get()
    print(docs.to_dict())
    info_doc = docs.to_dict()

    if info_doc:
        classification = info_doc['Classification']
        year = info_doc['Year']
        uni_name = info_doc['University Name']
        program = info_doc['Program Name']
        topic = info_doc['Topic']
        conference = info_doc['Conference']
        pay = info_doc['Pay']
    else:
        classification = ""
        year = ""
        uni_name = ""
        program = ""
        topic = ""
        conference = ""
        pay = ""

    # return render_template("Fa.html", grade=grade.title(), year=year, company_name=company_name,
    #                        pay=pay, position=position.title())
    return render_template("winterresearchForm.html", topic=topic, uni_name=uni_name, program=program,
                           conference=conference.title(), pay=pay, year=year, classification=classification)
    winterresearchbutton()


# return render_template("FallForm.html", grade=grade.title(), year = year, company_name = company_name, pay = pay, position = position.title())
# fallbutton()

@app.route('/winterresearchsurvey', methods=['POST', 'GET'])  # name of form
def winterresearch_survey():
    # cred = credentials.Certificate('firebase-sdk.json')
    # firebase_admin.initialize_app(cred)
    email = studentsignin.email
    # email = request.form['EMAIL']
    email = email.lower()
    email = email.title()
    id = ''
    if 'My.Fisk.Edu' in email:
        for i in email:
            if i != '@':
                id = id + i
            elif i == '@':
                break

    db = firestore.client()
    doc_ref = db.collection('student').document(str(id))
    research_info = doc_ref.collection('2022').document('Winter Research Experience Information')

    classification = request.form['CLASSIFICATION']
    uni_name = request.form['UNINAME']
    year = request.form['YEAR']
    conference = request.form['CONFERENCE']
    program = request.form['PROGRAM']
    pay = request.form['PAY']
    topic = request.form['TOPIC']

    research_info.set({
        'Fisk Email': str(email),
        'Classification': str(classification),
        'Year': str(year),
        'University Name': str(uni_name),
        'Program Name': str(program),
        'Topic': str(topic),
        'Conference': str(conference),
        'Pay': str(pay)
    })
    return render_template('Completedform.html')
    winterresearch_survey()


# #Post grad stuff!!!!!
@app.route('/postgrad_page')
def postgradbutton():
    fname = studentsignin.first_name
    lname = studentsignin.last_name
    email = studentsignin.email
    student_number = studentsignin.student_number
    major = studentsignin.major
    student_id = studentsignin.student_number
    return render_template("Postgradpage.html", firstname=fname, lastname=lname, fiskmajor=major, fiskemail=email,
                           studentNumber=student_number)
    return render_template("Postgradpage.html")

    postgradbutton()


# fulltime semester
@app.route('/fulltime_survey')
def fulltimebutton():
    userid = ''
    db = firestore.client()
    if 'My.Fisk.Edu' in studentsignin.email:
        for i in studentsignin.email:
            if i != '@':
                userid = userid + i
            elif i == '@':
                break

    doc_ref = db.collection('student').document(str(userid))
    docs = doc_ref.collection(str('2022')).get()
    docs = doc_ref.collection(str('2022')).document('Full-Time Information').get()

    info_doc = docs.to_dict()
    if info_doc:
        personal_email = info_doc['Personal Email']
        year = info_doc['Year']
        company_name = info_doc['Company Name']
        position = info_doc['Position']
        pay = info_doc['Salary']

    else:
        personal_email = ""
        year = ""
        company_name = ""
        pay = ""
        position = ""
    return render_template("fulltimeForm.html", personal_email=personal_email.capitalize(), year=year,
                           company_name=company_name, pay=pay, position=position.title())
    fulltimebutton()


@app.route('/')
def fulltime_form():
    return render_template('fulltimeForm.html')


@app.route('/fulltimesurvey', methods=['POST', 'GET'])  # name of form
def fulltime_survey():
    # cred = credentials.Certificate('firebase-sdk.json')
    # firebase_admin.initialize_app(cred)
    email = studentsignin.email
    # email = request.form['EMAIL']
    email = email.lower()
    email = email.title()
    id = ''
    if 'My.Fisk.Edu' in email:
        for i in email:
            if i != '@':
                id = id + i
            elif i == '@':
                break

    personal_email = request.form['PERSONAL_EMAIL']
    year = request.form['YEAR']
    company_name = request.form['COMPANYNAME']
    position = request.form['POSITION']
    pay = request.form['PAY']

    db = firestore.client()
    doc_ref = db.collection('student').document(str(id))
    fulltime_info = doc_ref.collection(str(year)).document('Full-Time Information')

    fulltime_info.set({
        'Personal Email': str(personal_email),
        'Year': str(year),
        'Company Name': str(company_name),
        'Position': str(position),
        'Salary': str(pay)
    })
    return render_template('Completedform.html')
    fulltime_survey()


# parttime
@app.route('/parttime_survey')
def parttimebutton():
    userid = ''
    db = firestore.client()
    if 'My.Fisk.Edu' in studentsignin.email:
        for i in studentsignin.email:
            if i != '@':
                userid = userid + i
            elif i == '@':
                break

    doc_ref = db.collection('student').document(str(userid))
    docs = doc_ref.collection(str('2022')).get()
    docs = doc_ref.collection(str('2022')).document('Part-Time Information').get()

    info_doc = docs.to_dict()
    if info_doc:
        personal_email = info_doc['Personal Email']
        year = info_doc['Year']
        company_name = info_doc['Company Name']
        position = info_doc['Position']
        pay = info_doc['Hourly Pay']

    else:
        personal_email = ""
        year = ""
        company_name = ""
        pay = ""
        position = ""
    return render_template("parttimeForm.html", personal_email=personal_email.capitalize(), year=year,
                           company_name=company_name, pay=pay, position=position.title())
    parttimebutton()


@app.route('/')
def parttime_form():
    return render_template('parttimeForm.html')


@app.route('/parttimesurvey', methods=['POST', 'GET'])  # name of form
def parttime_survey():
    # cred = credentials.Certificate('firebase-sdk.json')
    # firebase_admin.initialize_app(cred)
    email = studentsignin.email
    # email = request.form['EMAIL']
    email = email.lower()
    email = email.title()
    id = ''
    if 'My.Fisk.Edu' in email:
        for i in email:
            if i != '@':
                id = id + i
            elif i == '@':
                break

    personal_email = request.form['PERSONAL_EMAIL']
    year = request.form['YEAR']
    company_name = request.form['COMPANYNAME']
    position = request.form['POSITION']
    pay = request.form['PAY']

    db = firestore.client()
    doc_ref = db.collection('student').document(str(id))
    parttime_info = doc_ref.collection(str(year)).document('Part-Time Information')

    parttime_info.set({
        'Personal Email': str(personal_email),
        'Year': str(year),
        'Company Name': str(company_name),
        'Position': str(position),
        'Hourly Pay': str(pay)
    })
    return render_template('Completedform.html')
    parttime_survey()


# grad school
@app.route('/gradschool_survey')
def gradschoolbutton():
    userid = ''
    db = firestore.client()
    if 'My.Fisk.Edu' in studentsignin.email:
        for i in studentsignin.email:
            if i != '@':
                userid = userid + i
            elif i == '@':
                break

    doc_ref = db.collection('student').document(str(userid))
    docs = doc_ref.collection(str('2022')).get()
    docs = doc_ref.collection(str('2022')).document('Graduate School Information').get()

    info_doc = docs.to_dict()
    if info_doc:
        personal_email = info_doc['Personal Email']
        year = info_doc['Year']
        uni_name = info_doc['Graduate School']
        program = info_doc['Program Name']
        degree = info_doc['Degree']

    else:
        personal_email = ""
        year = ""
        uni_name = ""
        program = ""
        degree = ""
    return render_template("gradschoolForm.html", personal_email=personal_email, year=year, uni_name=uni_name,
                           program=program, degree=degree)


@app.route('/')
def gradschool_form():
    return render_template('gradschoolForm.html')


@app.route('/gradschoolsurvey', methods=['POST', 'GET'])  # name of form
def gradschool_survey():
    # cred = credentials.Certificate('firebase-sdk.json')
    # firebase_admin.initialize_app(cred)
    email = studentsignin.email
    # email = request.form['EMAIL']
    email = email.lower()
    email = email.title()
    id = ''
    if 'My.Fisk.Edu' in email:
        for i in email:
            if i != '@':
                id = id + i
            elif i == '@':
                break

    personal_email = request.form['PERSONAL_EMAIL']
    year = request.form['YEAR']
    uni_name = request.form['UNINAME']
    program = request.form['PROGRAM']
    degree = request.form['DEGREE']

    db = firestore.client()
    doc_ref = db.collection('student').document(str(id))
    grad_info = doc_ref.collection(str(year)).document('Graduate School Information')

    grad_info.set({
        'Personal Email': str(personal_email),
        'Year': str(year),
        'Graduate School': str(uni_name),
        'Program Name': str(program),
        'Degree': str(degree)
    })
    return render_template('Completedform.html')
    gradschool_survey()


# military school
@app.route('/military_survey')
def militarybutton():
    userid = ''
    db = firestore.client()
    if 'My.Fisk.Edu' in studentsignin.email:
        for i in studentsignin.email:
            if i != '@':
                userid = userid + i
            elif i == '@':
                break

    doc_ref = db.collection('student').document(str(userid))
    docs = doc_ref.collection(str('2022')).get()
    docs = doc_ref.collection(str('2022')).document('Military Service Information').get()

    info_doc = docs.to_dict()
    if info_doc:
        personal_email = info_doc['Personal Email']
        year = info_doc['Year']
        branch = info_doc['Branch']
        position = info_doc['Position']
        pay = info_doc['Pay']

    else:
        personal_email = ""
        year = ""
        branch = ""
        position = ""
        pay = ""
    return render_template("militaryForm.html", personal_email=personal_email, year=year, branch=branch,
                           position=position, pay=pay)
    militarybutton()


@app.route('/')
def military_form():
    return render_template('militaryForm.html')


@app.route('/militarysurvey', methods=['POST', 'GET'])  # name of form
def military_survey():
    # cred = credentials.Certificate('firebase-sdk.json')
    # firebase_admin.initialize_app(cred)
    email = studentsignin.email
    # email = request.form['EMAIL']
    email = email.lower()
    email = email.title()
    id = ''
    if 'My.Fisk.Edu' in email:
        for i in email:
            if i != '@':
                id = id + i
            elif i == '@':
                break

    personal_email = request.form['PERSONAL_EMAIL']
    year = request.form['YEAR']
    branch = request.form['BRANCH']
    position = request.form['POSITION']
    pay = request.form['PAY']

    db = firestore.client()
    doc_ref = db.collection('student').document(str(id))
    parttime_info = doc_ref.collection(str(year)).document('Military Service Information')

    parttime_info.set({
        'Personal Email': str(personal_email),
        'Year': str(year),
        'Branch': str(branch),
        'Position': str(position),
        'Pay': str(pay)
    })
    return render_template('Completedform.html')
    military_survey()


@app.route('/student-b2studentpage')
def b2studentpage():
    fname = studentsignin.first_name
    lname = studentsignin.last_name
    email = studentsignin.email
    major = studentsignin.major
    student_id = studentsignin.student_number
    return render_template("studentpage2.html", firstname=fname, lastname=lname, fiskmajor=major, fiskemail=email,
                           studentNumber=student_id)
    # return render_template('studentpage.html')
    b2studentpage()


# /////////////////////FACULTY SECTION///////////////////////////
@app.route('/faculty-b2facultypage')
def b2facultypage():
    fname = facultysignin.first_name
    lname = facultysignin.last_name
    email = facultysignin.email
    return render_template("facultypage2.html", firstname=fname, lastname=lname, fiskemail=email)
    # return render_template('studentpage.html')
    b2studentpage()


# faculty input
@app.route('/facultyinputpt1')
def facutyinputbutton():
    fname = facultysignin.first_name
    lname = facultysignin.last_name
    return render_template("facultyinputpt1.html", firstname=fname, lastname=lname)
    facutyinputbutton()


# ///////////////FALL///////////////////////////////
@app.route('/facultyfallsurvey')
def facultyfallbutton():
    return render_template('facultyfallinternshipfollowup.html')


@app.route('/facultyfall_internship_info')
def fallsearch():
    return render_template('fallsearchbar.html')


@app.route('/fallstudentsearchbar', methods=['POST', 'GET'])  # name of form
def studentsearchbar():
    userid = ''
    db = firestore.client()
    email = request.form['EMAIL']
    email = email.title()
    if 'My.Fisk.Edu' in email:
        for i in email:
            if i != '@':
                userid = userid + i
            elif i == '@':
                break

    doc_ref = db.collection('student').document(str(userid))
    docs = doc_ref.collection(str('2022')).get()
    docs = doc_ref.collection(str('2022')).document('Fall Internship Information').get()

    info_doc = docs.to_dict()
    if info_doc:
        result = db.collection('student').document(str(userid)).get()
        result = result.to_dict()
        first_name = result.get('First Name')
        first_name = first_name.lower()
        first_name = first_name.title()
        last_name = result.get('Last Name')
        last_name = last_name.lower()
        last_name = last_name.title()
        studentfullname = str(first_name) + " " + last_name

        return render_template("fallsearchbar2.html", email=email, studentfullname=studentfullname)
    else:
        return render_template("facultyfallsurvey.html")


@app.route('/')
def facultyfall_form():
    return render_template('facultyfallsurvey.html')


@app.route('/facultyfallsurvey', methods=['POST', 'GET'])  # name of form
def facultyfall_survey():
    email = facultysignin.email
    email = email.lower()
    email = email.title()

    db = firestore.client()
    userid = ''
    if 'Fisk.Edu' in email:
        for i in email:
            if i != '@':
                userid = userid + i
            elif i == '@':
                break

    result = db.collection('FacultyandStaff').document(str(userid)).get()
    result = result.to_dict()
    first_name = result.get('First Name')
    first_name = first_name.lower()
    first_name = first_name.title()
    last_name = result.get('Last Name')
    last_name = last_name.lower()
    last_name = last_name.title()
    facultyfullname = str(first_name) + " " + last_name

    # studentinfo
    email2 = request.form['EMAIL']
    email2 = email2.lower()
    email2 = email2.title()
    id = ''
    if 'My.Fisk.Edu' in email2:
        for i in email2:
            if i != '@':
                id = id + i
            elif i == '@':
                break

    student = ""
    db = firestore.client()
    studentfullname = request.form['NAME']
    classification = request.form['CLASSIFICATION']
    year = request.form['YEAR']
    company_name = request.form['COMPANYNAME']
    position = request.form['POSITION']
    pay = request.form['PAY']
    doc_ref = db.collection('student').document(str(id))
    fall_info = doc_ref.collection(str(year)).document('Fall Internship Information-Faculty Input')
    fall_info.set({
        'Note': "FACULTY INPUTTED DATA",
        'Faculty Name': str(facultyfullname),
        'Classification': str(classification),
        'Internship Year': str(year),
        'Company Name': str(company_name),
        'Position': str(position),
        'Hourly Pay': str(pay)

    })

    facultydoc_ref = db.collection('FacultyandStaff').document(str(userid))
    facultyfall_info = facultydoc_ref.collection(str(year)).document("Fall").collection(
        "('Faculty Input: Fall Internship Information").document(str(id))

    facultyfall_info.set({
        'Student Name': str(studentfullname),
        'Student UserName': str(id),
        'Classification': str(classification),
        'Internship Year': str(year),
        'Company Name': str(company_name),
        'Position': str(position),
        'Hourly Pay': str(pay)

    })

    return render_template('facultyCompletedForm.html', student=student)

    facultyfall_survey()


# fall research
@app.route('/facultyfallresearch_survey')
def fallresearch_search():
    return render_template('fallresearchsearchbar.html')


@app.route('/fallresearchstudentsearchbar', methods=['POST', 'GET'])  # name of form
def fallresearch_studentsearchbar():
    userid = ''
    db = firestore.client()
    email = request.form['EMAIL']
    email = email.title()
    if 'My.Fisk.Edu' in email:
        for i in email:
            if i != '@':
                userid = userid + i
            elif i == '@':
                break

    doc_ref = db.collection('student').document(str(userid))
    docs = doc_ref.collection(str('2022')).get()
    docs = doc_ref.collection(str('2022')).document('Fall Research Experience Information').get()

    info_doc = docs.to_dict()
    if info_doc:
        result = db.collection('student').document(str(userid)).get()
        result = result.to_dict()
        first_name = result.get('First Name')
        first_name = first_name.lower()
        first_name = first_name.title()
        last_name = result.get('Last Name')
        last_name = last_name.lower()
        last_name = last_name.title()
        studentfullname = str(first_name) + " " + last_name

        return render_template("fallresearchsearchbar2.html", email=email, studentfullname=studentfullname)
    else:
        return render_template("facultyfallresearchForm.html")


@app.route('/')
def facultyfallresearch_form():
    return render_template('facultyfallresearchForm.html')


@app.route('/facultyfallresearchsurvey', methods=['POST', 'GET'])  # name of form
def facultyfallresearch_survey():
    email = facultysignin.email
    email = email.lower()
    email = email.title()

    db = firestore.client()
    userid = ''
    if 'Fisk.Edu' in email:
        for i in email:
            if i != '@':
                userid = userid + i
            elif i == '@':
                break

    result = db.collection('FacultyandStaff').document(str(userid)).get()
    result = result.to_dict()
    first_name = result.get('First Name')
    first_name = first_name.lower()
    first_name = first_name.title()
    last_name = result.get('Last Name')
    last_name = last_name.lower()
    last_name = last_name.title()
    facultyfullname = str(first_name) + " " + last_name

    # studentinfo
    email2 = request.form['EMAIL']
    email2 = email2.lower()
    email2 = email2.title()
    id = ''
    if 'My.Fisk.Edu' in email2:
        for i in email2:
            if i != '@':
                id = id + i
            elif i == '@':
                break

    student = ""
    db = firestore.client()
    studentfullname = request.form['NAME']
    classification = request.form['CLASSIFICATION']
    uni_name = request.form['UNINAME']
    year = request.form['YEAR']
    conference = request.form['CONFERENCE']
    program = request.form['PROGRAM']
    pay = request.form['PAY']
    topic = request.form['TOPIC']
    doc_ref = db.collection('student').document(str(id))
    fallresearch_info = doc_ref.collection(str(year)).document('Fall Research Experience Information: Faculty Input')
    fallresearch_info.set({
        'Note': "FACULTY INPUTTED DATA",
        'Faculty Name': str(facultyfullname),
        'Classification': str(classification),
        'Year': str(year),
        'University Name': str(uni_name),
        'Program Name': str(program),
        'Topic': str(topic),
        'Conference': str(conference),
        'Pay': str(pay)

    })
    if 'My.Fisk.Edu' in email2:
        for i in email2:
            if i != '@':
                id = id + i
            elif i == '@':
                break

    facultydoc_ref = db.collection('FacultyandStaff').document(str(userid))
    facultyfallresearch_info = facultydoc_ref.collection(str(year)).document("Fall").collection(
        "Fall Research Experience Information: Faculty Input").document(str(id))

    # facultyfallresearch_info= facultyfallresearch_info.document(str(id))

    facultyfallresearch_info.set({
        'Student Name': str(studentfullname),
        'Student UserName': str(id),
        'Classification': str(classification),
        'Year': str(year),
        'University Name': str(uni_name),
        'Program Name': str(program),
        'Topic': str(topic),
        'Conference': str(conference),
        'Pay': str(pay)

    })
    return render_template('facultyCompletedForm.html', student=student)

    facultyfallresearch_survey()


# ////////////////////////////SPRING/////////////////////////////////////////////////////////

@app.route('/facultyspringsurvey')
def facultyspringbutton():
    return render_template('facultyspringinternshipfollowup.html')


@app.route('/facultyspring_internship_info')
def springsearch():
    return render_template('springsearchbar.html')


@app.route('/springstudentsearchbar', methods=['POST', 'GET'])  # name of form
def springstudentsearchbar():
    userid = ''
    db = firestore.client()
    email = request.form['EMAIL']
    email = email.title()
    if 'My.Fisk.Edu' in email:
        for i in email:
            if i != '@':
                userid = userid + i
            elif i == '@':
                break

    doc_ref = db.collection('student').document(str(userid))
    docs = doc_ref.collection(str('2022')).get()
    docs = doc_ref.collection(str('2022')).document('Spring Internship Information').get()

    info_doc = docs.to_dict()
    if info_doc:
        result = db.collection('student').document(str(userid)).get()
        result = result.to_dict()
        first_name = result.get('First Name')
        first_name = first_name.lower()
        first_name = first_name.title()
        last_name = result.get('Last Name')
        last_name = last_name.lower()
        last_name = last_name.title()
        studentfullname = str(first_name) + " " + last_name

        return render_template("springsearchbar2.html", email=email, studentfullname=studentfullname)
    else:
        return render_template("facultyspringsurvey.html")


@app.route('/')
def facultyspring_form():
    return render_template('facultyspringsurvey.html')


@app.route('/facultyspringsurvey', methods=['POST', 'GET'])  # name of form
def facultyspring_survey():
    email = facultysignin.email
    email = email.lower()
    email = email.title()

    db = firestore.client()
    userid = ''
    if 'Fisk.Edu' in email:
        for i in email:
            if i != '@':
                userid = userid + i
            elif i == '@':
                break

    result = db.collection('FacultyandStaff').document(str(userid)).get()
    result = result.to_dict()
    first_name = result.get('First Name')
    first_name = first_name.lower()
    first_name = first_name.title()
    last_name = result.get('Last Name')
    last_name = last_name.lower()
    last_name = last_name.title()
    facultyfullname = str(first_name) + " " + last_name

    # studentinfo
    email2 = request.form['EMAIL']
    email2 = email2.lower()
    email2 = email2.title()
    id = ''
    if 'My.Fisk.Edu' in email2:
        for i in email2:
            if i != '@':
                id = id + i
            elif i == '@':
                break

    student = ""
    db = firestore.client()
    studentfullname = request.form['NAME']
    classification = request.form['CLASSIFICATION']
    year = request.form['YEAR']
    company_name = request.form['COMPANYNAME']
    position = request.form['POSITION']
    pay = request.form['PAY']
    doc_ref = db.collection('student').document(str(id))
    fall_info = doc_ref.collection(str(year)).document('Spring Internship Information: Faculty Input')
    fall_info.set({
        'Note': "FACULTY INPUTTED DATA",
        'Faculty Name': str(facultyfullname),
        'Classification': str(classification),
        'Internship Year': str(year),
        'Company Name': str(company_name),
        'Position': str(position),
        'Hourly Pay': str(pay)

    })

    facultydoc_ref = db.collection('FacultyandStaff').document(str(userid))
    facultyfall_info = facultydoc_ref.collection(str(year)).document("Spring").collection(
        "('Faculty Input: Spring Internship Information").document(str(id))
    facultyfall_info.set({
        'Student Name': str(studentfullname),
        'Student UserName': str(id),
        'Classification': str(classification),
        'Internship Year': str(year),
        'Company Name': str(company_name),
        'Position': str(position),
        'Hourly Pay': str(pay)

    })

    return render_template('facultyCompletedForm.html', student=student)

    facultyspring_survey()


# SPRING research
@app.route('/facultyspringresearch_survey')
def springresearch_search():
    return render_template('springresearchsearchbar.html')


@app.route('/springresearchstudentsearchbar', methods=['POST', 'GET'])  # name of form
def springresearch_studentsearchbar():
    userid = ''
    db = firestore.client()
    email = request.form['EMAIL']
    email = email.title()
    if 'My.Fisk.Edu' in email:
        for i in email:
            if i != '@':
                userid = userid + i
            elif i == '@':
                break

    doc_ref = db.collection('student').document(str(userid))
    docs = doc_ref.collection(str('2022')).get()
    docs = doc_ref.collection(str('2022')).document('Spring Research Experience Information').get()

    info_doc = docs.to_dict()
    if info_doc:
        result = db.collection('student').document(str(userid)).get()
        result = result.to_dict()
        first_name = result.get('First Name')
        first_name = first_name.lower()
        first_name = first_name.title()
        last_name = result.get('Last Name')
        last_name = last_name.lower()
        last_name = last_name.title()
        studentfullname = str(first_name) + " " + last_name

        return render_template("springresearchsearchbar2.html", email=email, studentfullname=studentfullname)
    else:
        return render_template("facultyspringresearchForm.html")


@app.route('/')
def facultyspringresearch_form():
    return render_template('facultyspringresearchForm.html')


@app.route('/facultyspringresearchsurvey', methods=['POST', 'GET'])  # name of form
def facultyspringresearch_survey():
    email = facultysignin.email
    email = email.lower()
    email = email.title()

    db = firestore.client()
    userid = ''
    if 'Fisk.Edu' in email:
        for i in email:
            if i != '@':
                userid = userid + i
            elif i == '@':
                break

    result = db.collection('FacultyandStaff').document(str(userid)).get()
    result = result.to_dict()
    first_name = result.get('First Name')
    first_name = first_name.lower()
    first_name = first_name.title()
    last_name = result.get('Last Name')
    last_name = last_name.lower()
    last_name = last_name.title()
    facultyfullname = str(first_name) + " " + last_name

    # studentinfo
    email2 = request.form['EMAIL']
    email2 = email2.lower()
    email2 = email2.title()
    id = ''
    if 'My.Fisk.Edu' in email2:
        for i in email2:
            if i != '@':
                id = id + i
            elif i == '@':
                break

    student = ""
    db = firestore.client()
    studentfullname = request.form['NAME']
    classification = request.form['CLASSIFICATION']
    uni_name = request.form['UNINAME']
    year = request.form['YEAR']
    conference = request.form['CONFERENCE']
    program = request.form['PROGRAM']
    pay = request.form['PAY']
    topic = request.form['TOPIC']
    doc_ref = db.collection('student').document(str(id))
    springresearch_info = doc_ref.collection(str(year)).document(
        'Spring Research Experience Information: Faculty Input')
    springresearch_info.set({
        'Note': "FACULTY INPUTTED DATA",
        'Faculty Name': str(facultyfullname),
        'Classification': str(classification),
        'Year': str(year),
        'University Name': str(uni_name),
        'Program Name': str(program),
        'Topic': str(topic),
        'Conference': str(conference),
        'Pay': str(pay)

    })
    if 'My.Fisk.Edu' in email2:
        for i in email2:
            if i != '@':
                id = id + i
            elif i == '@':
                break

    facultydoc_ref = db.collection('FacultyandStaff').document(str(userid))
    facultyspringresearch_info = facultydoc_ref.collection(str(year)).document("Spring").collection(
        "Spring Research Experience Information: Faculty Input").document(str(id))

    # facultyfallresearch_info= facultyfallresearch_info.document(str(id))

    facultyspringresearch_info.set({
        'Student Name': str(studentfullname),
        'Student UserName': str(id),
        'Classification': str(classification),
        'Year': str(year),
        'University Name': str(uni_name),
        'Program Name': str(program),
        'Topic': str(topic),
        'Conference': str(conference),
        'Pay': str(pay)

    })
    return render_template('facultyCompletedForm.html', student=student)

    facultyspringresearch_survey()


# //////////////////////////SUMMER///////////////////////////

@app.route('/facultysummersurvey')
def facultysummerbutton():
    return render_template('facultysummerinternshipfollowup.html')


@app.route('/facultysummer_internship_info')
def summersearch():
    return render_template('summersearchbar.html')


@app.route('/summerstudentsearchbar', methods=['POST', 'GET'])  # name of form
def summerstudentsearchbar():
    userid = ''
    db = firestore.client()
    email = request.form['EMAIL']
    email = email.title()
    if 'My.Fisk.Edu' in email:
        for i in email:
            if i != '@':
                userid = userid + i
            elif i == '@':
                break

    doc_ref = db.collection('student').document(str(userid))
    docs = doc_ref.collection(str('2022')).get()
    docs = doc_ref.collection(str('2022')).document('Summer Internship Information').get()

    info_doc = docs.to_dict()
    if info_doc:
        result = db.collection('student').document(str(userid)).get()
        result = result.to_dict()
        first_name = result.get('First Name')
        first_name = first_name.lower()
        first_name = first_name.title()
        last_name = result.get('Last Name')
        last_name = last_name.lower()
        last_name = last_name.title()
        studentfullname = str(first_name) + " " + last_name

        return render_template("summersearchbar2.html", email=email, studentfullname=studentfullname)
    else:
        return render_template("facultysummersurvey.html")


@app.route('/')
def facultysummer_form():
    return render_template('facultysummersurvey.html')


@app.route('/facultysummersurvey', methods=['POST', 'GET'])  # name of form
def facultysummer_survey():
    email = facultysignin.email
    email = email.lower()
    email = email.title()

    db = firestore.client()
    userid = ''
    if 'Fisk.Edu' in email:
        for i in email:
            if i != '@':
                userid = userid + i
            elif i == '@':
                break

    result = db.collection('FacultyandStaff').document(str(userid)).get()
    result = result.to_dict()
    first_name = result.get('First Name')
    first_name = first_name.lower()
    first_name = first_name.title()
    last_name = result.get('Last Name')
    last_name = last_name.lower()
    last_name = last_name.title()
    facultyfullname = str(first_name) + " " + last_name

    # studentinfo
    email2 = request.form['EMAIL']
    email2 = email2.lower()
    email2 = email2.title()
    id = ''
    if 'My.Fisk.Edu' in email2:
        for i in email2:
            if i != '@':
                id = id + i
            elif i == '@':
                break

    student = ""
    db = firestore.client()
    studentfullname = request.form['NAME']
    classification = request.form['CLASSIFICATION']
    year = request.form['YEAR']
    company_name = request.form['COMPANYNAME']
    position = request.form['POSITION']
    pay = request.form['PAY']
    doc_ref = db.collection('student').document(str(id))
    summer_info = doc_ref.collection(str(year)).document('Summer Internship Information: Faculty Input')
    summer_info.set({
        'Note': "FACULTY INPUTTED DATA",
        'Faculty Name': str(facultyfullname),
        'Classification': str(classification),
        'Internship Year': str(year),
        'Company Name': str(company_name),
        'Position': str(position),
        'Hourly Pay': str(pay)

    })

    facultydoc_ref = db.collection('FacultyandStaff').document(str(userid))
    facultysummer_info = facultydoc_ref.collection(str(year)).document("Summer").collection(
        "('Faculty Input: Summer Internship Information").document(str(id))
    facultysummer_info.set({
        'Student Name': str(studentfullname),
        'Student UserName': str(id),
        'Classification': str(classification),
        'Internship Year': str(year),
        'Company Name': str(company_name),
        'Position': str(position),
        'Hourly Pay': str(pay)

    })

    return render_template('facultyCompletedForm.html', student=student)

    facultyfall_survey()


# summer research
@app.route('/facultysummerresearch_survey')
def summerresearch_search():
    return render_template('summerresearchsearchbar.html')


@app.route('/summerresearchstudentsearchbar', methods=['POST', 'GET'])  # name of form
def summerresearch_studentsearchbar():
    userid = ''
    db = firestore.client()
    email = request.form['EMAIL']
    email = email.title()
    if 'My.Fisk.Edu' in email:
        for i in email:
            if i != '@':
                userid = userid + i
            elif i == '@':
                break

    doc_ref = db.collection('student').document(str(userid))
    docs = doc_ref.collection(str('2022')).get()
    docs = doc_ref.collection(str('2022')).document('Summer Research Experience Information').get()

    info_doc = docs.to_dict()
    if info_doc:
        result = db.collection('student').document(str(userid)).get()
        result = result.to_dict()
        first_name = result.get('First Name')
        first_name = first_name.lower()
        first_name = first_name.title()
        last_name = result.get('Last Name')
        last_name = last_name.lower()
        last_name = last_name.title()
        studentfullname = str(first_name) + " " + last_name

        return render_template("summerresearchsearchbar2.html", email=email, studentfullname=studentfullname)
    else:
        return render_template("facultysummerresearchForm.html")


@app.route('/')
def facultysummerresearch_form():
    return render_template('facultysummerresearchForm.html')


@app.route('/facultysummerresearchsurvey', methods=['POST', 'GET'])  # name of form
def facultysummerresearch_survey():
    email = facultysignin.email
    email = email.lower()
    email = email.title()

    db = firestore.client()
    userid = ''
    if 'Fisk.Edu' in email:
        for i in email:
            if i != '@':
                userid = userid + i
            elif i == '@':
                break

    result = db.collection('FacultyandStaff').document(str(userid)).get()
    result = result.to_dict()
    first_name = result.get('First Name')
    first_name = first_name.lower()
    first_name = first_name.title()
    last_name = result.get('Last Name')
    last_name = last_name.lower()
    last_name = last_name.title()
    facultyfullname = str(first_name) + " " + last_name

    # studentinfo
    email2 = request.form['EMAIL']
    email2 = email2.lower()
    email2 = email2.title()
    id = ''
    if 'My.Fisk.Edu' in email2:
        for i in email2:
            if i != '@':
                id = id + i
            elif i == '@':
                break

    student = ""
    db = firestore.client()
    studentfullname = request.form['NAME']
    classification = request.form['CLASSIFICATION']
    uni_name = request.form['UNINAME']
    year = request.form['YEAR']
    conference = request.form['CONFERENCE']
    program = request.form['PROGRAM']
    pay = request.form['PAY']
    topic = request.form['TOPIC']
    doc_ref = db.collection('student').document(str(id))
    summerresearch_info = doc_ref.collection(str(year)).document(
        'Summer Research Experience Information: Faculty Input')
    summerresearch_info.set({
        'Note': "FACULTY INPUTTED DATA",
        'Faculty Name': str(facultyfullname),
        'Classification': str(classification),
        'Year': str(year),
        'University Name': str(uni_name),
        'Program Name': str(program),
        'Topic': str(topic),
        'Conference': str(conference),
        'Pay': str(pay)

    })
    if 'My.Fisk.Edu' in email2:
        for i in email2:
            if i != '@':
                id = id + i
            elif i == '@':
                break

    facultydoc_ref = db.collection('FacultyandStaff').document(str(userid))
    facultysummerresearch_info = facultydoc_ref.collection(str(year)).document("Summer").collection(
        "Summer Research Experience Information: Faculty Input").document(str(id))
    # facultyfallresearch_info= facultyfallresearch_info.document(str(id))

    facultysummerresearch_info.set({
        'Student Name': str(studentfullname),
        'Student UserName': str(id),
        'Classification': str(classification),
        'Year': str(year),
        'University Name': str(uni_name),
        'Program Name': str(program),
        'Topic': str(topic),
        'Conference': str(conference),
        'Pay': str(pay)

    })
    return render_template('facultyCompletedForm.html', student=student)

    facultysummerresearch_survey()


# ////////////////////WINTER////////////////////////////////////

@app.route('/facultywintersurvey')
def facultywinterbutton():
    return render_template('facultywinterinternshipfollowup.html')


@app.route('/facultywinter_internship_info')
def wintersearch():
    return render_template('wintersearchbar.html')


@app.route('/winterstudentsearchbar', methods=['POST', 'GET'])  # name of form
def winterstudentsearchbar():
    userid = ''
    db = firestore.client()
    email = request.form['EMAIL']
    email = email.title()
    if 'My.Fisk.Edu' in email:
        for i in email:
            if i != '@':
                userid = userid + i
            elif i == '@':
                break

    doc_ref = db.collection('student').document(str(userid))
    docs = doc_ref.collection(str('2022')).get()
    docs = doc_ref.collection(str('2022')).document('Winter Internship Information').get()

    info_doc = docs.to_dict()
    if info_doc:
        result = db.collection('student').document(str(userid)).get()
        result = result.to_dict()
        first_name = result.get('First Name')
        first_name = first_name.lower()
        first_name = first_name.title()
        last_name = result.get('Last Name')
        last_name = last_name.lower()
        last_name = last_name.title()
        studentfullname = str(first_name) + " " + last_name

        return render_template("wintersearchbar2.html", email=email, studentfullname=studentfullname)
    else:
        return render_template("facultywintersurvey.html")


@app.route('/')
def facultywinter_form():
    return render_template('facultywintersurvey.html')


@app.route('/facultywintersurvey', methods=['POST', 'GET'])  # name of form
def facultywinter_survey():
    email = facultysignin.email
    email = email.lower()
    email = email.title()

    db = firestore.client()
    userid = ''
    if 'Fisk.Edu' in email:
        for i in email:
            if i != '@':
                userid = userid + i
            elif i == '@':
                break

    result = db.collection('FacultyandStaff').document(str(userid)).get()
    result = result.to_dict()
    first_name = result.get('First Name')
    first_name = first_name.lower()
    first_name = first_name.title()
    last_name = result.get('Last Name')
    last_name = last_name.lower()
    last_name = last_name.title()
    facultyfullname = str(first_name) + " " + last_name

    # studentinfo
    email2 = request.form['EMAIL']
    email2 = email2.lower()
    email2 = email2.title()
    id = ''
    if 'My.Fisk.Edu' in email2:
        for i in email2:
            if i != '@':
                id = id + i
            elif i == '@':
                break

    student = ""
    db = firestore.client()
    studentfullname = request.form['NAME']
    classification = request.form['CLASSIFICATION']
    year = request.form['YEAR']
    company_name = request.form['COMPANYNAME']
    position = request.form['POSITION']
    pay = request.form['PAY']
    doc_ref = db.collection('student').document(str(id))
    winter_info = doc_ref.collection(str(year)).document('Winter Internship Information: Faculty Input')
    winter_info.set({
        'Note': "FACULTY INPUTTED DATA",
        'Faculty Name': str(facultyfullname),
        'Classification': str(classification),
        'Internship Year': str(year),
        'Company Name': str(company_name),
        'Position': str(position),
        'Hourly Pay': str(pay)

    })

    facultydoc_ref = db.collection('FacultyandStaff').document(str(userid))
    facultywinter_info = facultydoc_ref.collection(str(year)).document("Winter").collection(
        "('Faculty Input: Winter Internship Information").document(str(id))
    facultywinter_info.set({
        'Student Name': str(studentfullname),
        'Student UserName': str(id),
        'Classification': str(classification),
        'Internship Year': str(year),
        'Company Name': str(company_name),
        'Position': str(position),
        'Hourly Pay': str(pay)

    })

    return render_template('facultyCompletedForm.html', student=student)

    facultyfall_survey()


# winter research
@app.route('/facultywinterresearch_survey')
def winterresearch_search():
    return render_template('winterresearchsearchbar.html')


@app.route('/winterresearchstudentsearchbar', methods=['POST', 'GET'])  # name of form
def winterresearch_studentsearchbar():
    userid = ''
    db = firestore.client()
    email = request.form['EMAIL']
    email = email.title()
    if 'My.Fisk.Edu' in email:
        for i in email:
            if i != '@':
                userid = userid + i
            elif i == '@':
                break

    doc_ref = db.collection('student').document(str(userid))
    docs = doc_ref.collection(str('2022')).get()
    docs = doc_ref.collection(str('2022')).document('Winter Research Experience Information').get()

    info_doc = docs.to_dict()
    if info_doc:
        result = db.collection('student').document(str(userid)).get()
        result = result.to_dict()
        first_name = result.get('First Name')
        first_name = first_name.lower()
        first_name = first_name.title()
        last_name = result.get('Last Name')
        last_name = last_name.lower()
        last_name = last_name.title()
        studentfullname = str(first_name) + " " + last_name

        return render_template("winterresearchsearchbar2.html", email=email, studentfullname=studentfullname)
    else:
        return render_template("facultywinterresearchForm.html")


@app.route('/')
def facultywinterresearch_form():
    return render_template('facultywinterresearchForm.html')


@app.route('/facultywinterresearchsurvey', methods=['POST', 'GET'])  # name of form
def facultywinterresearch_survey():
    email = facultysignin.email
    email = email.lower()
    email = email.title()

    db = firestore.client()
    userid = ''
    if 'Fisk.Edu' in email:
        for i in email:
            if i != '@':
                userid = userid + i
            elif i == '@':
                break

    result = db.collection('FacultyandStaff').document(str(userid)).get()
    result = result.to_dict()
    first_name = result.get('First Name')
    first_name = first_name.lower()
    first_name = first_name.title()
    last_name = result.get('Last Name')
    last_name = last_name.lower()
    last_name = last_name.title()
    facultyfullname = str(first_name) + " " + last_name

    # studentinfo
    email2 = request.form['EMAIL']
    email2 = email2.lower()
    email2 = email2.title()
    id = ''
    if 'My.Fisk.Edu' in email2:
        for i in email2:
            if i != '@':
                id = id + i
            elif i == '@':
                break

    student = ""
    db = firestore.client()
    studentfullname = request.form['NAME']
    classification = request.form['CLASSIFICATION']
    uni_name = request.form['UNINAME']
    year = request.form['YEAR']
    conference = request.form['CONFERENCE']
    program = request.form['PROGRAM']
    pay = request.form['PAY']
    topic = request.form['TOPIC']
    doc_ref = db.collection('student').document(str(id))
    winterresearch_info = doc_ref.collection(str(year)).document(
        'Winter Research Experience Information: Faculty Input')
    winterresearch_info.set({
        'Note': "FACULTY INPUTTED DATA",
        'Faculty Name': str(facultyfullname),
        'Classification': str(classification),
        'Year': str(year),
        'University Name': str(uni_name),
        'Program Name': str(program),
        'Topic': str(topic),
        'Conference': str(conference),
        'Pay': str(pay)

    })
    if 'My.Fisk.Edu' in email2:
        for i in email2:
            if i != '@':
                id = id + i
            elif i == '@':
                break

    facultydoc_ref = db.collection('FacultyandStaff').document(str(userid))
    facultywinterresearch_info = facultydoc_ref.collection(str(year)).document("Winter").collection(
        "Winter Research Experience Information: Faculty Input").document(str(id))
    # facultyfallresearch_info= facultyfallresearch_info.document(str(id))

    facultywinterresearch_info.set({
        'Student Name': str(studentfullname),
        'Student UserName': str(id),
        'Classification': str(classification),
        'Year': str(year),
        'University Name': str(uni_name),
        'Program Name': str(program),
        'Topic': str(topic),
        'Conference': str(conference),
        'Pay': str(pay)

    })
    return render_template('facultyCompletedForm.html', student=student)

    facultywinterresearch_survey()


# ////////////////// #Post grad stuff!!!!!!!!!!!!!!!!!!!!!
@app.route('/facultypostgrad_page')
def facultypostgradbutton():
    fname = facultysignin.first_name
    lname = facultysignin.last_name
    return render_template("FacultyPostgradpage.html", firstname=fname, lastname=lname)
    facultypostgradbutton()


# fulltime
@app.route('/facultyfulltime_survey')
def fulltimesearch():
    return render_template('fulltimesearchbar.html')


@app.route('/fulltimestudentsearchbar', methods=['POST', 'GET'])  # name of form
def fulltimestudentsearchbar():
    userid = ''
    db = firestore.client()
    email = request.form['EMAIL']
    email = email.title()
    if 'My.Fisk.Edu' in email:
        for i in email:
            if i != '@':
                userid = userid + i
            elif i == '@':
                break

    doc_ref = db.collection('student').document(str(userid))
    docs = doc_ref.collection(str('2022')).get()
    docs = doc_ref.collection(str('2022')).document('Full-Time Information').get()

    info_doc = docs.to_dict()
    if info_doc:
        result = db.collection('student').document(str(userid)).get()
        result = result.to_dict()
        first_name = result.get('First Name')
        first_name = first_name.lower()
        first_name = first_name.title()
        last_name = result.get('Last Name')
        last_name = last_name.lower()
        last_name = last_name.title()
        studentfullname = str(first_name) + " " + last_name

        return render_template("fulltimesearchbar2.html", email=email, studentfullname=studentfullname)
    else:
        return render_template("facultyfulltimeForm.html")


# def facutyfallinputbutton():
#     return render_template("facultyfallsurvey.html")
#     facutyfallinputbutton()
@app.route('/')
def facultyfulltime_form():
    return render_template('facultyfulltimeForm.html')


@app.route('/facultyfulltimesurvey', methods=['POST', 'GET'])  # name of form
def facultyfulltime_survey():
    email = facultysignin.email
    email = email.lower()
    email = email.title()

    db = firestore.client()
    userid = ''
    if 'Fisk.Edu' in email:
        for i in email:
            if i != '@':
                userid = userid + i
            elif i == '@':
                break

    result = db.collection('FacultyandStaff').document(str(userid)).get()
    result = result.to_dict()
    first_name = result.get('First Name')
    first_name = first_name.lower()
    first_name = first_name.title()
    last_name = result.get('Last Name')
    last_name = last_name.lower()
    last_name = last_name.title()
    facultyfullname = str(first_name) + " " + last_name

    # studentinfo
    email2 = request.form['EMAIL']
    email2 = email2.lower()
    email2 = email2.title()
    id = ''
    if 'My.Fisk.Edu' in email2:
        for i in email2:
            if i != '@':
                id = id + i
            elif i == '@':
                break

    student = ""
    db = firestore.client()
    studentfullname = request.form['NAME']
    fisk_email = request.form['EMAIL']
    personal_email = request.form['PERSONAL_EMAIL']
    year = request.form['YEAR']
    company_name = request.form['COMPANYNAME']
    position = request.form['POSITION']
    pay = request.form['PAY']
    doc_ref = db.collection('student').document(str(id))
    fulltime_info = doc_ref.collection(str(year)).document('Full-Time Information: Faculty Input')
    fulltime_info.set({
        'Note': "FACULTY INPUTTED DATA",
        'Faculty Name': str(facultyfullname),
        'Fisk Email': str(fisk_email),
        'Personal Email': str(personal_email),
        'Year': str(year),
        'Company Name': str(company_name),
        'Position': str(position),
        'Salary': str(pay)

    })

    facultydoc_ref = db.collection('FacultyandStaff').document(str(userid))
    facultyfulltime_info = facultydoc_ref.collection(str(year)).document("Post Graduate Opportunity").collection(
        "Full Time Opportunity: Faculty Input").document(str(id))
    facultyfulltime_info.set({
        'Student Name': str(studentfullname),
        'Student UserName': str(id),
        'Fisk Email': str(fisk_email),
        'Personal Email': str(personal_email),
        'Year': str(year),
        'Company Name': str(company_name),
        'Position': str(position),
        'Salary': str(pay)

    })

    return render_template('facultyCompletedForm.html', student=student)


# parttime
@app.route('/facultyparttime_survey')
def partimesearch():
    return render_template('parttimesearchbar.html')


@app.route('/parttimestudentsearchbar', methods=['POST', 'GET'])  # name of form
def parttimestudentsearchbar():
    userid = ''
    db = firestore.client()
    email = request.form['EMAIL']
    email = email.title()
    if 'My.Fisk.Edu' in email:
        for i in email:
            if i != '@':
                userid = userid + i
            elif i == '@':
                break

    doc_ref = db.collection('student').document(str(userid))
    docs = doc_ref.collection(str('2022')).get()
    docs = doc_ref.collection(str('2022')).document('Part-Time Information').get()

    info_doc = docs.to_dict()
    if info_doc:
        result = db.collection('student').document(str(userid)).get()
        result = result.to_dict()
        first_name = result.get('First Name')
        first_name = first_name.lower()
        first_name = first_name.title()
        last_name = result.get('Last Name')
        last_name = last_name.lower()
        last_name = last_name.title()
        studentfullname = str(first_name) + " " + last_name

        return render_template("parttimesearchbar2.html", email=email, studentfullname=studentfullname)
    else:
        return render_template("facultyparttimeForm.html")


# def facutyfallinputbutton():
#     return render_template("facultyfallsurvey.html")
#     facutyfallinputbutton()
@app.route('/')
def facultypartime_form():
    return render_template('facultyparttimeForm.html')


@app.route('/facultyparttimesurvey', methods=['POST', 'GET'])  # name of form
def facultyparttime_survey():
    email = facultysignin.email
    email = email.lower()
    email = email.title()

    db = firestore.client()
    userid = ''
    if 'Fisk.Edu' in email:
        for i in email:
            if i != '@':
                userid = userid + i
            elif i == '@':
                break

    result = db.collection('FacultyandStaff').document(str(userid)).get()
    result = result.to_dict()
    first_name = result.get('First Name')
    first_name = first_name.lower()
    first_name = first_name.title()
    last_name = result.get('Last Name')
    last_name = last_name.lower()
    last_name = last_name.title()
    facultyfullname = str(first_name) + " " + last_name

    # studentinfo
    email2 = request.form['EMAIL']
    email2 = email2.lower()
    email2 = email2.title()
    id = ''
    if 'My.Fisk.Edu' in email2:
        for i in email2:
            if i != '@':
                id = id + i
            elif i == '@':
                break

    student = ""
    db = firestore.client()
    studentfullname = request.form['NAME']
    fisk_email = request.form['EMAIL']
    personal_email = request.form['PERSONAL_EMAIL']
    year = request.form['YEAR']
    company_name = request.form['COMPANYNAME']
    position = request.form['POSITION']
    pay = request.form['PAY']
    doc_ref = db.collection('student').document(str(id))
    parttime_info = doc_ref.collection(str(year)).document('Part-Time Information: Faculty Input')
    parttime_info.set({
        'Note': "FACULTY INPUTTED DATA",
        'Faculty Name': str(facultyfullname),
        'Fisk Email': str(fisk_email),
        'Personal Email': str(personal_email),
        'Year': str(year),
        'Company Name': str(company_name),
        'Position': str(position),
        'Hourly Pay': str(pay)

    })

    facultydoc_ref = db.collection('FacultyandStaff').document(str(userid))
    facultyparttime_info = facultydoc_ref.collection(str(year)).document("Post Graduate Opportunity").collection(
        "Part-Time Opportunity: Faculty Input").document(str(id))
    facultyparttime_info.set({
        'Student Name': str(studentfullname),
        'Student UserName': str(id),
        'Fisk Email': str(fisk_email),
        'Personal Email': str(personal_email),
        'Year': str(year),
        'Company Name': str(company_name),
        'Position': str(position),
        'Hourly Pay': str(pay)

    })

    return render_template('facultyCompletedForm.html', student=student)


# military
@app.route('/facultymilitary_survey')
def militarysearch():
    return render_template('militarysearchbar.html')


@app.route('/militarystudentsearchbar', methods=['POST', 'GET'])  # name of form
def militarystudentsearchbar():
    userid = ''
    db = firestore.client()
    email = request.form['EMAIL']
    email = email.title()
    if 'My.Fisk.Edu' in email:
        for i in email:
            if i != '@':
                userid = userid + i
            elif i == '@':
                break

    doc_ref = db.collection('student').document(str(userid))
    docs = doc_ref.collection(str('2022')).get()
    docs = doc_ref.collection(str('2022')).document('Military Service Information').get()

    info_doc = docs.to_dict()
    if info_doc:
        result = db.collection('student').document(str(userid)).get()
        result = result.to_dict()
        first_name = result.get('First Name')
        first_name = first_name.lower()
        first_name = first_name.title()
        last_name = result.get('Last Name')
        last_name = last_name.lower()
        last_name = last_name.title()
        studentfullname = str(first_name) + " " + last_name

        return render_template("militarysearchbar2.html", email=email, studentfullname=studentfullname)
    else:
        return render_template("facultymilitaryForm.html")


# def facutyfallinputbutton():
#     return render_template("facultyfallsurvey.html")
#     facutyfallinputbutton()
@app.route('/')
def facultymilitary_form():
    return render_template('facultymilitaryForm.html')


@app.route('/facultymilitarysurvey', methods=['POST', 'GET'])  # name of form
def facultymilitary_survey():
    email = facultysignin.email
    email = email.lower()
    email = email.title()

    db = firestore.client()
    userid = ''
    if 'Fisk.Edu' in email:
        for i in email:
            if i != '@':
                userid = userid + i
            elif i == '@':
                break

    result = db.collection('FacultyandStaff').document(str(userid)).get()
    result = result.to_dict()
    first_name = result.get('First Name')
    first_name = first_name.lower()
    first_name = first_name.title()
    last_name = result.get('Last Name')
    last_name = last_name.lower()
    last_name = last_name.title()
    facultyfullname = str(first_name) + " " + last_name

    # studentinfo
    email2 = request.form['EMAIL']
    email2 = email2.lower()
    email2 = email2.title()
    id = ''
    if 'My.Fisk.Edu' in email2:
        for i in email2:
            if i != '@':
                id = id + i
            elif i == '@':
                break

    student = ""
    db = firestore.client()
    studentfullname = request.form['NAME']
    fisk_email = request.form['EMAIL']
    personal_email = request.form['PERSONAL_EMAIL']
    year = request.form['YEAR']
    branch = request.form['BRANCH']
    position = request.form['POSITION']
    pay = request.form['PAY']
    doc_ref = db.collection('student').document(str(id))
    military_info = doc_ref.collection(str(year)).document('Military Service Information: Faculty Input')
    military_info.set({
        'Note': "FACULTY INPUTTED DATA",
        'Faculty Name': str(facultyfullname),
        'Fisk Email': str(fisk_email),
        'Personal Email': str(personal_email),
        'Year': str(year),
        'Branch': str(branch),
        'Position': str(position),
        'Pay': str(pay)

    })

    facultydoc_ref = db.collection('FacultyandStaff').document(str(userid))
    military_info = facultydoc_ref.collection(str(year)).document("Post Graduate Opportunity").collection(
        "Military Opportunity: Faculty Input").document(str(id))
    military_info.set({
        'Student Name': str(studentfullname),
        'Student UserName': str(id),
        'Fisk Email': str(fisk_email),
        'Personal Email': str(personal_email),
        'Year': str(year),
        'Branch': str(branch),
        'Position': str(position),
        'Pay': str(pay)

    })

    return render_template('facultyCompletedForm.html', student=student)


# gradschool
@app.route('/facultygradschool_survey')
def gradschoolsearch():
    return render_template('gradschoolsearchbar.html')


@app.route('/gradschoolstudentsearchbar', methods=['POST', 'GET'])  # name of form
def gradschoolstudentsearchbar():
    userid = ''
    db = firestore.client()
    email = request.form['EMAIL']
    email = email.title()
    if 'My.Fisk.Edu' in email:
        for i in email:
            if i != '@':
                userid = userid + i
            elif i == '@':
                break

    doc_ref = db.collection('student').document(str(userid))
    docs = doc_ref.collection(str('2022')).get()
    docs = doc_ref.collection(str('2022')).document('Graduate School Information').get()

    info_doc = docs.to_dict()
    if info_doc:
        result = db.collection('student').document(str(userid)).get()
        result = result.to_dict()
        first_name = result.get('First Name')
        first_name = first_name.lower()
        first_name = first_name.title()
        last_name = result.get('Last Name')
        last_name = last_name.lower()
        last_name = last_name.title()
        studentfullname = str(first_name) + " " + last_name

        return render_template("gradschoolsearchbar2.html", email=email, studentfullname=studentfullname)
    else:
        return render_template("facultygradschoolForm.html")


# def facutyfallinputbutton():
#     return render_template("facultyfallsurvey.html")
#     facutyfallinputbutton()
@app.route('/')
def facultygradschool_form():
    return render_template('facultygradschoolForm.html')


@app.route('/facultygradschoolsurvey', methods=['POST', 'GET'])  # name of form
def facultygradschool_survey():
    email = facultysignin.email
    email = email.lower()
    email = email.title()

    db = firestore.client()
    userid = ''
    if 'Fisk.Edu' in email:
        for i in email:
            if i != '@':
                userid = userid + i
            elif i == '@':
                break

    result = db.collection('FacultyandStaff').document(str(userid)).get()
    result = result.to_dict()
    first_name = result.get('First Name')
    first_name = first_name.lower()
    first_name = first_name.title()
    last_name = result.get('Last Name')
    last_name = last_name.lower()
    last_name = last_name.title()
    facultyfullname = str(first_name) + " " + last_name

    # studentinfo
    email2 = request.form['EMAIL']
    email2 = email2.lower()
    email2 = email2.title()
    id = ''
    if 'My.Fisk.Edu' in email2:
        for i in email2:
            if i != '@':
                id = id + i
            elif i == '@':
                break

    student = ""
    db = firestore.client()
    studentfullname = request.form['NAME']
    fisk_email = request.form['EMAIL']
    personal_email = request.form['PERSONAL_EMAIL']
    year = request.form['YEAR']
    uni_name = request.form['UNINAME']
    program = request.form['PROGRAM']
    degree = request.form['DEGREE']
    doc_ref = db.collection('student').document(str(id))
    gradschool_info = doc_ref.collection(str(year)).document('Graduate School Information: Faculty Input')
    gradschool_info.set({
        'Note': "FACULTY INPUTTED DATA",
        'Faculty Name': str(facultyfullname),
        'Fisk Email': str(fisk_email),
        'Personal Email': str(personal_email),
        'Year': str(year),
        'Graduate School': str(uni_name),
        'Program Name': str(program),
        'Degree': str(degree)
    })

    facultydoc_ref = db.collection('FacultyandStaff').document(str(userid))
    facultygradschool_info = facultydoc_ref.collection(str(year)).document("Post Graduate Opportunity").collection(
        "Graduate School Opportunity: Faculty Input").document(str(id))
    facultygradschool_info.set({
        'Student Name': str(studentfullname),
        'Student UserName': str(id),
        'Fisk Email': str(fisk_email),
        'Personal Email': str(personal_email),
        'Year': str(year),
        'Graduate School': str(uni_name),
        'Program Name': str(program),
        'Degree': str(degree)

    })

    return render_template('facultyCompletedForm.html', student=student)

# /////////////////////FACULTY RETRIEVE DATA////////////////////////////////////////
@app.route('/retrievedata')
def facultyretrievedata():
    fname = facultysignin.first_name
    lname = facultysignin.last_name
    return render_template("dataoptions.html", firstname=fname, lastname=lname)
    facultyretrievedata()


@app.route('/individual_data')
def individualretrievedata():
    fname = facultysignin.first_name
    lname = facultysignin.last_name
    return render_template("Individualstudentchecker.html")
    individualretrievedata()



@app.route('/singlestudentchecker', methods=['POST', 'GET'])  # name of form
def individualdatareport():
    db = firestore.client()
    userid = ''
    fisk_email = request.form['EMAIL']
    fisk_email = fisk_email.title()
    year = request.form['YEAR']
    semester = request.form['SEMESTER']
    Opportunity = request.form['OPPORTUNITY']
    if 'My.Fisk.Edu' in fisk_email:
        for i in fisk_email:
            if i != '@':
                userid = userid + i
            elif i == '@':
                break
        result = db.collection('student').document(str(userid)).get()
        result = result.to_dict()
        fname = result.get('First Name')
        fname = fname.lower()
        fname = fname.title()
        lname = result.get('Last Name')
        lname = lname.lower()
        lname= lname.title()

    doc_ref = db.collection('student').document(str(userid))
    docs = doc_ref.collection(str(year)).get()
    # print(docs.to_dict())
    # info_doc = docs.to_dict()
    if Opportunity == "Undergraduate: Internship Opportunity" and semester == "Fall":
        docs = doc_ref.collection(str(year)).document('Fall Internship Information').get()
        info_doc = docs.to_dict()
        if info_doc:
            grade = info_doc['Classification']
            year = info_doc['Internship Year']
            company_name = info_doc['Company Name']
            pay = info_doc['Hourly Pay']
            position = info_doc['Position']
            return render_template("singlestudentresultspage.html", Opportunity=Opportunity, fname=fname,
                                   semester=semester,
                                   lname=lname, fisk_email=fisk_email, grade=grade.title(), year=year,
                                   company_name=company_name, pay=pay, position=position.title())
        else:
            return render_template("NoIndividualstudentchecker.html", Opportunity=Opportunity, fisk_email=fisk_email, year=year, semester=semester)
            print(Opportunity)

    if Opportunity == "Undergraduate: Internship Opportunity" and semester == "Spring":
        docs = doc_ref.collection(str(year)).document('Spring Internship Information').get()
        info_doc = docs.to_dict()
        if info_doc:
            grade = info_doc['Classification']
            year = info_doc['Internship Year']
            company_name = info_doc['Company Name']
            pay = info_doc['Hourly Pay']
            position = info_doc['Position']
            return render_template("singlestudentresultspage.html", Opportunity=Opportunity, fname=fname,
                                   semester=semester,
                                   lname=lname, fisk_email=fisk_email, grade=grade.title(), year=year,
                                   company_name=company_name, pay=pay, position=position.title())
        else:
            return render_template("NoIndividualstudentchecker.html", Opportunity=Opportunity, fisk_email=fisk_email,
                                   year=year, semester=semester)



    if Opportunity == "Undergraduate: Internship Opportunity" and semester == "Summer":
        docs = doc_ref.collection(str(year)).document('Summer Internship Information').get()
        info_doc = docs.to_dict()
        if info_doc:
            grade = info_doc['Classification']
            year = info_doc['Internship Year']
            company_name = info_doc['Company Name']
            pay = info_doc['Hourly Pay']
            position = info_doc['Position']
            return render_template("singlestudentresultspage.html", Opportunity=Opportunity, fname=fname,
                                   semester=semester,
                                   lname=lname, fisk_email=fisk_email, grade=grade.title(), year=year,
                                   company_name=company_name, pay=pay, position=position.title())
        else:
            return render_template("NoIndividualstudentchecker.html", Opportunity=Opportunity, fisk_email=fisk_email,
                                   year=year, semester=semester)
    if Opportunity == "Undergraduate: Internship Opportunity" and semester == "Winter":
        docs = doc_ref.collection(str(year)).document('Winter Internship Information').get()
        info_doc = docs.to_dict()
        if info_doc:
            grade = info_doc['Classification']
            year = info_doc['Internship Year']
            company_name = info_doc['Company Name']
            pay = info_doc['Hourly Pay']
            position = info_doc['Position']
            return render_template("singlestudentresultspage.html", Opportunity=Opportunity, fname=fname,
                                   semester=semester,
                                   lname=lname, fisk_email=fisk_email, grade=grade.title(), year=year,
                                   company_name=company_name, pay=pay, position=position.title())
        else:
            return render_template("NoIndividualstudentchecker.html", Opportunity=Opportunity, fisk_email=fisk_email, year=year, semester=semester)

    if Opportunity == "Undergraduate: Research Experience" and semester == "Fall":
        docs = doc_ref.collection(str(year)).document('Fall Research Experience Information').get()
        info_doc = docs.to_dict()
        if info_doc:
            classification = info_doc['Classification']
            year = info_doc['Year']
            uni_name = info_doc['University Name']
            program = info_doc['Program Name']
            topic = info_doc['Topic']
            conference = info_doc['Conference']
            pay = info_doc['Pay']
        else:
            classification = ""
            year = ""
            uni_name = ""
            program = ""
            topic = ""
            conference = ""
            pay = ""
        return render_template("researchsinglestudentresultspage.html", Opportunity=Opportunity, fname=fname, semester=semester,
                               lname=lname, fisk_email=fisk_email, year=year, uni_name= uni_name,program=program,
                               topic= topic,  conference= conference, pay=pay)

    if Opportunity == "Undergraduate: Research Experience" and semester == "Spring":
        docs = doc_ref.collection(str(year)).document('Spring Research Experience Information').get()
        info_doc = docs.to_dict()
        if info_doc:
            classification = info_doc['Classification']
            year = info_doc['Year']
            uni_name = info_doc['University Name']
            program = info_doc['Program Name']
            topic = info_doc['Topic']
            conference = info_doc['Conference']
            pay = info_doc['Pay']
            return render_template("researchsinglestudentresultspage.html", Opportunity=Opportunity, fname=fname,
                                   semester=semester,
                                   lname=lname, fisk_email=fisk_email, year=year, uni_name=uni_name, program=program,
                                   topic=topic, conference=conference, pay=pay)
        else:
            return render_template("NoIndividualstudentchecker.html", Opportunity=Opportunity, fisk_email=fisk_email,
                                   year=year, semester=semester)



    if Opportunity == "Undergraduate: Research Experience" and semester == "Summer":
        docs = doc_ref.collection(str(year)).document('Summer Research Experience Information').get()
        info_doc = docs.to_dict()
        if info_doc:
            classification = info_doc['Classification']
            year = info_doc['Year']
            uni_name = info_doc['University Name']
            program = info_doc['Program Name']
            topic = info_doc['Topic']
            conference = info_doc['Conference']
            pay = info_doc['Pay']
            return render_template("researchsinglestudentresultspage.html", Opportunity=Opportunity, fname=fname,
                                   semester=semester,
                                   lname=lname, fisk_email=fisk_email, year=year, uni_name=uni_name, program=program,
                                   topic=topic, conference=conference, pay=pay)
        else:
            return render_template("NoIndividualstudentchecker.html", Opportunity=Opportunity, fisk_email=fisk_email,
                                   year=year, semester=semester)


    if Opportunity == "Undergraduate: Research Experience" and semester == "Winter":
        docs = doc_ref.collection(str(year)).document('Winter Research Experience Information').get()
        info_doc = docs.to_dict()
        if info_doc:
            classification = info_doc['Classification']
            year = info_doc['Year']
            uni_name = info_doc['University Name']
            program = info_doc['Program Name']
            topic = info_doc['Topic']
            conference = info_doc['Conference']
            pay = info_doc['Pay']
            return render_template("researchsinglestudentresultspage.html", Opportunity=Opportunity, fname=fname,
                                   semester=semester,
                                   lname=lname, fisk_email=fisk_email, year=year, uni_name=uni_name, program=program,
                                   topic=topic, conference=conference, pay=pay)
        else:
            return render_template("NoIndividualstudentchecker.html", Opportunity=Opportunity, fisk_email=fisk_email,
                                   year=year, semester=semester)


    if Opportunity == "Post Graduate: Full Time Opportunity":
        docs = doc_ref.collection(str(year)).document('Full-Time Information').get()
        info_doc = docs.to_dict()
        if info_doc:
            personal_email = info_doc['Personal Email']
            year = info_doc['Year']
            company_name = info_doc['Company Name']
            position = info_doc['Position']
            pay = info_doc['Salary']
            return render_template("fulltimesinglestudentresultspage.html", Opportunity=Opportunity, fname=fname,
                                   semester=semester, lname=lname, fisk_email=fisk_email, personal_email=personal_email,
                                   year=year, company_name=company_name, position=position, pay=pay)

        else:
            return render_template("NoIndividualstudentchecker.html", Opportunity=Opportunity, fisk_email=fisk_email,
                                   year=year, semester=semester)

    if Opportunity == "Post Graduate: Part Time Opportunity":
        docs = doc_ref.collection(str(year)).document('Part-Time Information').get()
        info_doc = docs.to_dict()
        if info_doc:
            personal_email = info_doc['Personal Email']
            year = info_doc['Year']
            company_name = info_doc['Company Name']
            position = info_doc['Position']
            pay = info_doc['Hourly Pay']
            return render_template("parttimesinglestudentresultspage.html", Opportunity=Opportunity, fname=fname,
                                   semester=semester, lname=lname, fisk_email=fisk_email, personal_email=personal_email,
                                   year=year, company_name=company_name, position=position, pay=pay)
        else:
            return render_template("NoIndividualstudentchecker.html", Opportunity=Opportunity, fisk_email=fisk_email,
                                   year=year, semester=semester)

    if Opportunity == "Post Graduate: Military Opportunity":
        docs = doc_ref.collection(str(year)).document('Military Service Information').get()
        info_doc = docs.to_dict()
        if info_doc:
            personal_email = info_doc['Personal Email']
            year = info_doc['Year']
            branch = info_doc['Branch']
            position = info_doc['Position']
            pay = info_doc['Pay']
            return render_template("militarysinglestudentresultspage.html", Opportunity=Opportunity, fname=fname,
                                   semester=semester, lname=lname, fisk_email=fisk_email, personal_email=personal_email,
                                   year=year, branch=branch, position=position, pay=pay)

        else:
            return render_template("NoIndividualstudentchecker.html", Opportunity=Opportunity, fisk_email=fisk_email,
                                   year=year, semester=semester)



    if Opportunity == "Post Graduate: Graduate School Opportunity":
        docs = doc_ref.collection(str(year)).document('Graduate School Information').get()
        info_doc = docs.to_dict()
        if info_doc:
            personal_email = info_doc['Personal Email']
            year = info_doc['Year']
            uni_name = info_doc['Graduate School']
            program = info_doc['Program Name']
            degree = info_doc['Degree']
            return render_template("gradschoolsinglestudentresultspage.html", Opportunity=Opportunity, fname=fname,
                                   semester=semester, lname=lname, fisk_email=fisk_email, personal_email=personal_email,
                                   year=year, uni_name=uni_name, program=program, degree=degree)

        else:
            return render_template("NoIndividualstudentchecker.html", Opportunity=Opportunity, fisk_email=fisk_email,
                                   year=year, semester=semester)

    # return render_template("singlestudentresultspage.html")
    individualdatareport()


@app.route('/group_data')
def groupretrievedata():
    # fname = facultysignin.first_name
    # lname = facultysignin.last_name
    return render_template("groupstudentchecker.html")
    groupretrievedata()





if __name__ == "__main__":
    app.run(debug=True)