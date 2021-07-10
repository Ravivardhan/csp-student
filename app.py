from flask import Flask,render_template,request,redirect,url_for,session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import random
import os
import pyrebase
app=Flask(__name__)

app.secret_key='success'
app.config['MYSQL_HOST']='185.28.21.1'
app.config['MYSQL_USER']='u320202036_mentor'
app.config['MYSQL_PORT']=3306
app.config['MYSQL_PASSWORD']='Conzura9346@'
app.config['MYSQL_DB']='u320202036_mentor'
mysql=MySQL(app)
firebaseConfig = {
    'apiKey': "AIzaSyD4ACVVz74KKvZBAJWEvXDSOKObD_r_Bo8",
    'authDomain': "python-firebase-4feb8.firebaseapp.com",
    'databaseURL': "https://python-firebase-4feb8-default-rtdb.firebaseio.com/",
    'projectId': "python-firebase-4feb8",
    'storageBucket': "python-firebase-4feb8.appspot.com",
    'messagingSenderId': "370096610883",
    'appId': "1:370096610883:web:4b2754541584d867563ef6",
    'measurementId': "G-QSB7FJ0ZVX"
  }

firebase=pyrebase.initialize_app(firebaseConfig)
storage=firebase.storage()



@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    session.pop('username', None)
    session.pop('loggedin', None)
    session.pop('mentor_team',None)
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select * from accounts where username='{}' and password='{}'".format(username, password))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['username'] = request.form['username']
            cursor.execute("select teamname from accounts where username='{}'".format(session['username']))
            teamname=cursor.fetchone()
            for i in teamname:
                session['teamname']=i
                return render_template('home.html')
        else:
            msg = 'incorrect username or password'

    return render_template('log.html', msg=msg)


@app.route('/register', methods=['POST', 'GET'])
def register():
    session.pop('username', None)
    session.pop('loggedin', None)
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'email' in request.form and 'password' in request.form and 'confirm_password' in request.form:
        username = request.form['username']
        password = request.form['password']
        conf_psd = request.form['confirm_password']
        email = request.form['email']
        
        if password == conf_psd:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("select * from accounts where username='{}' and password='{}'".format(username, password))
            account = cursor.fetchone()
            if account:
                msg = "username already exists"
                return render_template('register.html', msg1=msg)
            cursor.execute("select * from accounts where email='{}'".format(email))
            mail = cursor.fetchone()
            if mail:
                msg = "email already taken"
                render_template('register.html', msg1=msg)

            if email.split('@')[1] != "srit.ac.in":
                msg="invalid email address"
                return render_template("register.html",msg1=msg)
            else:


                cursor.execute(
                    "insert into accounts(username,password,email) values('{}','{}','{}')".format(username, password,
                                                                                                  email))
                mysql.connection.commit()
                session['username'] = request.form['username']
                return render_template('home.html')

        if request.method == 'POST' and (request.form['password'] != request.form['confirm_password']):

                msg = "password didn't match"
                render_template('register.html', msg1=msg)
    return render_template('register.html')
@app.route('/home')
def home():
    return render_template('home.html')



@app.route('/home/team_verify')
def team_verify():
    database = MySQLdb.connect(host="185.28.21.1", user="u320202036_mentor", password="Conzura9346@", database="u320202036_mentor", port=3306)

    cursor = database.cursor()
    cursor.execute("select project from accounts where username='{}'".format(session['username']))
    p = cursor.fetchone()
    cursor.execute("select teamname from accounts where username='{}'".format(session['username']))
    table=cursor.fetchone()
    for i in p:
        if i != None:
            for i in table:
                database =MySQLdb.connect(host="185.28.21.1", user="u320202036_student", password="Conzura9346@", database="u320202036_student", port=3306)
                cursor = database.cursor()
                cursor.execute("select team_members,roll_no,branch from {}".format(i))
                data=cursor.fetchall()
                cursor.execute("select project from team_manage where teamname='{}'".format(i))
                project=cursor.fetchone()
                for i in project:
                    return render_template('mentor_team.html',table=data,project=i)
        else:
            return team()
@app.route('/home/project')
def project():
    database =MySQLdb.connect(host="185.28.21.1", user="u320202036_mentor", password="Conzura9346@", database="u320202036_mentor", port=3306)

    cursor = database.cursor()
    cursor.execute("select teamname from accounts where username='{}'".format(session['username']))
    team=cursor.fetchone()
    if team[0]!=None:


        database = MySQLdb.connect(host="185.28.21.1", user="u320202036_student", password="Conzura9346@", database="u320202036_student", port=3306)
        cursor = database.cursor()
        cursor.execute("select proj_sub from team_manage where mentor='{}'".format(session['username']))
        submission=cursor.fetchone()
        db = MySQLdb.connect(host="185.28.21.1", user="u320202036_mentor", password="Conzura9346@", database="u320202036_mentor", port=3306)

        c = db.cursor()
        c.execute("select teamname from accounts where username='{}'".format(session['username']))
        teamname=c.fetchone()
        print(submission)
        print(teamname)
        c.execute("select download from project_files where teamname='{}'".format(teamname[0]))
        downloaded = c.fetchone()
        database.commit()
        print(downloaded)
        if downloaded ==None:
            return render_template('index.html')
        if downloaded[0] == 'yes':
            conn = MySQLdb.connect(host="185.28.21.1", user="u320202036_mentor", password="Conzura9346@",
                                   database="u320202036_mentor", port=3306)

            cur = conn.cursor()

            # cur.execute("update project_files set download='yes' where teamname='{}'".format(i))
            cur.execute("select id from project_files where teamname='{}'".format(team[0]))
            id = cur.fetchone()

            for i in id:
                cur.execute("select file_name from project_files where id='{}'".format(i))
                filename = cur.fetchone()
                conn.commit()

                for i in filename:
                    print(str(i)[1:])

                    url = storage.child('images').child(str(i)[:]).get_url(None)
                    print(url)
            return render_template('completed.html',link=url)

        elif submission[0]=='yes':

            print(storage.child(teamname[0]).get_url(None))

            conn =MySQLdb.connect(host="185.28.21.1", user="u320202036_mentor", password="Conzura9346@", database="u320202036_mentor", port=3306)


            cur = conn.cursor()
            cur.execute("select teamname from accounts where username='{}'".format(session['username']))
            teamname = cur.fetchone()
            for i in teamname:
                teamn=i
                # cur.execute("update project_files set download='yes' where teamname='{}'".format(i))
                cur.execute("select id from project_files where teamname='{}'".format(i))
                id = cur.fetchone()

                for i in id:
                    cur.execute("select file_name from project_files where id='{}'".format(i))
                    filename = cur.fetchone()
                    conn.commit()

                    for i in filename:
                        print(str(i)[1:])

                        url = storage.child('images').child(str(i)[:]).get_url(None)
                        print(url)
                        conn4 = MySQLdb.connect(host="185.28.21.1", user="u320202036_student", password="Conzura9346@",
                                               database="u320202036_student", port=3306)
                        cu=conn4.cursor()
                        cu.execute("update team_manage set link='{}' where teamname='{}'".format(url,teamn))
                        conn4.commit()

            return render_template('project.html',link=url)
    if team[0]==None:
        return render_template('no_team.html')




@app.route('/home/project/final',methods=['POST','GET'])
def final():
    remarks=request.form['remarks']
    marks=request.form['marks']
    if remarks!=None and marks!=None:
        conn = MySQLdb.connect(host="185.28.21.1", user="u320202036_mentor", password="Conzura9346@", database="u320202036_mentor", port=3306)

        cur = conn.cursor()
        cur.execute("select teamname from accounts where username='{}'".format(session['username']))
        teamname=cur.fetchone()

        cur.execute("update  project_files set marks='{}' where teamname='{}'".format(marks,teamname[0]))
        cur.execute("update  project_files set remarks='{}' where teamname='{}'".format(remarks, teamname[0]))
        cur.execute("update project_files set download='yes' where teamname='{}'".format(teamname[0]))
        conn.commit()
        conn = MySQLdb.connect(host="185.28.21.1", user="u320202036_student", password="Conzura9346@", database="u320202036_student", port=3306)
        cursor=conn.cursor()
        cursor.execute("update team_manage set marks='{}'  where mentor='{}'".format(marks,session['username']) )
        conn.commit()

        for i in teamname:
            teamn = i
            # cur.execute("update project_files set download='yes' where teamname='{}'".format(i))
            cur.execute("select id from project_files where teamname='{}'".format(i))
            id = cur.fetchone()

            for i in id:
                cur.execute("select file_name from project_files where id='{}'".format(i))
                filename = cur.fetchone()
                conn.commit()

                for i in filename:
                    print(str(i)[1:])

                    url = storage.child('images').child(str(i)[:]).get_url(None)
                    print(url)
        return render_template('completed.html',link=url)






@app.route('/home/project/download',methods=['POST','GET'])
def download():
    if request.method=='POST':
        #####################import MySQLdb

        def write_file(data, filename):
            # Convert binary data to proper format and write it on Hard Disk
            with open(filename, 'wb') as file:
                file.write(data)

        def readBLOB(emp_id, photo):
            print("Reading BLOB data from python_employee table")

            try:
                connection =MySQLdb.connect(host="185.28.21.1", user="u320202036_mentor", password="Conzura9346@", database="u320202036_mentor", port=3306)


                cursor = connection.cursor()
                sql_fetch_blob_query = 'SELECT * from project_files where id = %s'

                cursor.execute(sql_fetch_blob_query, (emp_id,))
                record = cursor.fetchall()
                for row in record:
                    print("Id = ", row[0], )
                    print("Name = ", row[1])
                    image = row[2]
                    file = row[3]

                    write_file(image, photo)


                return render_template('downloaded.html')

            except ArithmeticError as error:
                print("Failed to read BLOB data from MySQL table {}".format(error))

        conn = MySQLdb.connect(host="185.28.21.1", user="u320202036_mentor", password="Conzura9346@", database="u320202036_mentor", port=3306)


        cur = conn.cursor()
        cur.execute("select teamname from accounts where username='{}'".format(session['username']))
        teamname=cur.fetchone()
        for i in teamname:
            teamn=i
            #cur.execute("update project_files set download='yes' where teamname='{}'".format(i))
            cur.execute("select id from project_files where teamname='{}'".format(i))
            id=cur.fetchone()

            for i in id:
                cur.execute("select file_name from project_files where id='{}'".format(i))
                filename=cur.fetchone()
                conn.commit()
                for name in filename:

                    url=storage.child("images/{}".format(name)).get_url()
                    print(url)
                    readBLOB(i, 'project_files/{}'.format(name))
                    os.path.abspath('project_files/{}'.format(name))


    return render_template('downloaded.html')

@app.route('/home/team')
def team():
    database = MySQLdb.connect(host="185.28.21.1", user="u320202036_student", password="Conzura9346@", database="u320202036_student", port=3306)
    cursor = database.cursor()
    cursor.execute("select teamname,project from team_manage where mentor ='None'")
    data=cursor.fetchall()
    database.commit()
    cursor.execute("select teamname from team_manage where mentor='None'")
    teams=cursor.fetchall()
    return render_template('team.html',data=data,teams=teams)
@app.route('/home/team/mentor_team',methods=['GET','POST'])
def mentor_team():
            team=request.form['selection']


            session['mentor_team']=team
            database = MySQLdb.connect(host="185.28.21.1", user="u320202036_mentor", password="Conzura9346@", database="u320202036_mentor", port=3306)

            cursor = database.cursor()
            cursor.execute("update accounts set teamname='{}' where username='{}'".format(team,session['username']))

            db =MySQLdb.connect(host="185.28.21.1", user="u320202036_student", password="Conzura9346@", database="u320202036_student", port=3306)
            cursor2 = db.cursor()
            cursor2.execute("update team_manage set mentor='{}' where teamname='{}'".format(session['username'],session['mentor_team']))
            cursor2.execute("select project from team_manage where teamname='{}'".format(session['mentor_team']))
            project=cursor2.fetchone()
            db.commit()
            for i in project:
                cursor.execute("update accounts set project='{}' where username='{}'".format(i,session['username']))
                database.commit()
                return render_template('index.html',project=i)
@app.route('/home/project/marks',methods=['POST','GET'])
def marks():
    if request.method=='POST':
        marks_by_mentor=request.form['marks']
        if len(marks_by_mentor)!=0:
            database = MySQLdb.connect(host="185.28.21.1", user="u320202036_student", password="Conzura9346@", database="u320202036_student", port=3306)
            cursor = database.cursor()
            db =MySQLdb.connect(host="185.28.21.1", user="u320202036_mentor", password="Conzura9346@", database="u320202036_mentor", port=3306)
            c=db.cursor()
            c.execute("select teamname from accounts where username='{}'".format(session['username']))
            teamname=c.fetchone()
            for i in teamname:
                cursor.execute("update team_manage set marks='{}' where teamname='{}'".format(marks_by_mentor,i))
            database.commit()
            return render_template("completed.html")

@app.route('/account')
def account():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select username ,email ,password from accounts where username='{}'".format(session['username']))
    data=cursor.fetchone()
    return render_template('account.html',username=data['username'],email=data['email'],password=data['password'])
@app.route('/change_password',methods=['POST','GET'])
def change_password():

    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    password=request.form['new_psd']
    cursor.execute("update accounts set password='{}' where username='{}'".format(password,session['username']))
    mysql.connection.commit()
    return account()
@app.route('/logout',methods=['POST','GET'])
def logout():
    session.pop('username',None)
    session.pop('loggedin',None)
    session.pop('mentor_team',None)
    return login()
if __name__ == '__main__':
    app.debug=True
    app.secret_key='success'
    app.run()