from flask import *
from turtle import st
from flask import Flask, render_template, request, redirect, url_for, session
from markupsafe import escape

import ibm_db
import sendgrid
import os
from sendgrid.helpers.mail import *
#sendgrid key
sg = sendgrid.SendGridAPIClient(api_key='*************************************') 

#Database Connection
conn = ibm_db.connect("*************************************************************************************",'','')

app = Flask(__name__)

#Register Page

@app.route('/',methods = ['POST', 'GET'])
def register():
  msg = ' '
  if request.method == 'POST':
    username = request.form['username']
    email = request.form['email']
    bloodgroup=request.form['bloodgroup']
    password = request.form['password']

    sql = "SELECT * FROM users WHERE email =?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,email)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    if account:
      msg = 'Account already exists !'
    elif not username or not password or not email:
      msg = 'Please fill the Missing Details !'
    
    else:
      insert_sql = "INSERT INTO users VALUES (?,?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, username)
      ibm_db.bind_param(prep_stmt, 2, email)
      ibm_db.bind_param(prep_stmt, 3, bloodgroup)
      ibm_db.bind_param(prep_stmt, 4, password)
      ibm_db.execute(prep_stmt)
      msg = 'Account created successfully '

      from_email = Email("praba3043@gmail.com")
      to_email = To(email)
      subject = "Sending with SendGrid is Fun from Praba"
      content = Content("text/plain", "and easy to do anywhere, even with Python")
      mail = Mail(from_email, to_email, subject, content)
      response = sg.client.mail.send.post(request_body=mail.get())
      print(response.status_code)
      print(response.body)
      print(response.headers)
 
      return render_template('login.html',msg=msg)
  return render_template('login.html',msg=msg)


#Login Page

@app.route('/login',methods = ['POST', 'GET'])
def login():
  msg = ' '
  if request.method == 'POST':
    email = request.form['email']
    password = request.form['password']     
    sql = "SELECT * FROM users WHERE Email =?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,email)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_both(stmt)    
    accounts=account   
    if (account):
      if(password == accounts['PASSWORD']):
        msg = 'Logged in successfully !'
        return render_template('index.html',msg=msg)
      else :
        msg='Wrong Credentials'
  return  render_template('login.html',msg=msg)  

#Donor Information 

@app.route('/requestform',methods = ['POST','GET'])
def requestform():
  msg = ' '
  if request.method == 'POST':
    username = request.form['username']
    age = request.form['age']
    gender = request.form['gender']
    bloodgroup= request.form['bloodgroup']
    email = request.form['email']
    address=request.form['address']
    city = request.form['city']
    pincode = request.form['pincode']
    contactno = request.form['contactno']

    sql = "SELECT * FROM receiver WHERE username =?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,username)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)

    if account:
      msg = 'Request already sent!'
    
    elif not username or not bloodgroup or not email or not contactno or not address or not city or not pincode or not gender or not age:
      msg = 'Please fill the Missing Details !'
    
    else:
      insert_sql = "INSERT INTO receiver VALUES (?,?,?,?,?,?,?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, username)
      ibm_db.bind_param(prep_stmt, 2, age)
      ibm_db.bind_param(prep_stmt, 3, gender)
      ibm_db.bind_param(prep_stmt, 4, bloodgroup)
      ibm_db.bind_param(prep_stmt, 5, email)
      ibm_db.bind_param(prep_stmt, 6, address)
      ibm_db.bind_param(prep_stmt, 7, city)
      ibm_db.bind_param(prep_stmt, 8, pincode)
      ibm_db.bind_param(prep_stmt, 9, contactno)
      ibm_db.execute(prep_stmt)
      msg = 'Request sent successfully'
      return render_template('index.html',msg=msg)
  return render_template('donate.html',msg=msg)

#List Page

@app.route('/list')
def list():
  users = []
  sql = "SELECT * FROM receiver"
  stmt = ibm_db.exec_immediate(conn, sql)
  dictionary = ibm_db.fetch_both(stmt)
  while dictionary != False:
    
    users.append(dictionary)
    dictionary = ibm_db.fetch_both(stmt)

  if users:
    return render_template("list.html",users = users)

  return "success..."  

#Sending E-Mail to Donor

@app.route('/success/<email>')
def success(email):
  
  
  from_email = Email("praba3043@gmail.com")
  to_email = To(email)
  subject = "From SharingJoy request for donor"
  
  content = f'http://127.0.0.1:5000/donorsuccess'
  mail = Mail(from_email, to_email, subject, content)
  response = sg.client.mail.send.post(request_body=mail.get())
  print(response.status_code)
  print(response.body)
  print(response.headers)
  return render_template("success.html") 
  

@app.route('/donorsuccess')
def donorsuccess():
  return render_template("donorsuccess.html")

#Acceptance form

@app.route('/accept',methods = ['POST', 'GET']) 
def accept():
  if request.method == 'POST':
    username = request.form['username']
    insert_sql = "INSERT INTO acceptorname VALUES (?)"
    prep_stmt = ibm_db.prepare(conn, insert_sql)
    ibm_db.bind_param(prep_stmt, 1, username)
      
    ibm_db.execute(prep_stmt)
    
    
    return render_template("donorsuccess.html")



@app.route('/acceptlist')
def acceptlist():
  users = []
  sql = "SELECT * FROM acceptorname"
  stmt = ibm_db.exec_immediate(conn, sql)
  dictionary = ibm_db.fetch_both(stmt)
  while dictionary != False:
    
    users.append(dictionary)
    dictionary = ibm_db.fetch_both(stmt)

  if users:
    return render_template("acceptlist.html",users = users)    

#After donated Deleted Successfully

@app.route('/delete/<username>')
def delete(username):
  sql = f"SELECT * FROM acceptorname WHERE username='{escape(username)}'"
  print(sql)
  stmt = ibm_db.exec_immediate(conn, sql)
  donation = ibm_db.fetch_row(stmt)
  
  if donation:
    sql = f"DELETE FROM acceptorname WHERE username='{escape(username)}'"
   
    stmt = ibm_db.exec_immediate(conn, sql)

    donation = []
    sql = "SELECT * FROM acceptorname"
    stmt = ibm_db.exec_immediate(conn, sql)
    dictionary = ibm_db.fetch_both(stmt)
    while dictionary != False:
      donation.append(dictionary)
      dictionary = ibm_db.fetch_both(stmt)
    if donation:
      return redirect("/acceptlist")


     

    
   
  



if __name__ == '__main__':
    app.run(debug=True)