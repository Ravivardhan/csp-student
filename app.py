from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors

app=Flask(__name__)
app.secret_key='success'
import pyrebase
app.secret_key='success'
app.config['MYSQL_HOST']='185.28.21.1'
app.config['MYSQL_USER']='u320202036_student'
app.config['MYSQL_PORT']=3306
app.config['MYSQL_PASSWORD']='Conzura9346@'
app.config['MYSQL_DB']='u320202036_student'
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
@app.route('/year',methods=['POST',"GET"])
def year():
    global student_year
    if request.method=='POST':
        session['year']=request.form['student-year']


        return render_template('log.html')
    return render_template('year.html')

@app.route('/login',methods=['GET','POST'])
def login():

    session.pop('username',None)
    session.pop('loggedin',None)
    msg=''
    if request.method=='POST' and 'username' in request.form and 'password' in request.form:
        username=request.form['username']
        password=request.form['password']
        cursor= mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select * from accounts where username='{}' and password='{}'".format(username,password))

        account=cursor.fetchone()
        if account:
            session['loggedin']=True
            session['username']=request.form['username']
            cursor.execute("select teamname from accounts where username='{}'".format(session['username']))
            teamname = cursor.fetchone()
            for i in teamname:
                session['teamname'] = i
            cursor.execute("select year from accounts where username='{}'".format(session['username']))
            y=cursor.fetchone()
            print(y['year'])
            if int(y['year'])==int(session['year']):


                    return render_template('homepage.html')
            else:
                flash(u'Incorrect Year provided...', 'error')

        else:
            msg='incorrect username or password'
            flash(u'Invalid password provided', 'error')

    return render_template('log.html',msg=msg)
@app.route('/register',methods=['POST','GET'])
def register():
    session.pop('username',None)
    session.pop('loggedin',None)
    msg=''
    if request.method=='POST' and 'username' in request.form and 'email' in request.form and 'password' in request.form and 'confirm_password' in request.form  :
        username=request.form['username']
        password=request.form['password']
        conf_psd=request.form['confirm_password']
        email=request.form['email']
        branch=request.form['student-year']
        roll_no=request.form['roll_no']
        if roll_no!=None and branch!=None:
                if password==conf_psd:
                    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute("select * from accounts where username='{}' and password='{}'".format(username,password))
                    account=cursor.fetchone()
                    if account:
                        msg="username already exists"
                        flash(u'username already exists', 'error')

                        return render_template('register.html',msg=msg)
                    cursor.execute("select * from accounts where email='{}'".format(email))
                    mail=cursor.fetchone()
                    if mail:
                        msg="email already taken"
                        flash(u'email already taken', 'error')

                        render_template('register.html',msg=msg)
                    if request.method == 'POST' and (request.form['password'] != request.form['confirm_password']):

                        msg = "password didn't match"
                        flash(u'password didnt match', 'error')

                        render_template('register.html',msg=msg)


                    else:
                        if email.split('@')[1] == "srit.ac.in":
                            cursor.execute(
                                "insert into accounts(username,password,email,year,branch,roll_no) values('{}','{}','{}', '{}','{}','{}')".format(
                                    username, password, email, session['year'], branch, roll_no))
                            mysql.connection.commit()
                            session['username'] = request.form['username']
                            session['loggedin'] = True

                            return render_template('homepage.html')
                        else:
                            return render_template("register.html",msg="not a valid email")


        
    return  render_template('register.html',msg=msg)
@app.route('/homepage')
def homepage():
    return render_template('homepage.html')
@app.route('/homepage/team_view')
def team_view():
    database =MySQLdb.connect(host="185.28.21.1", user="u320202036_student", password="Conzura9346@", database="u320202036_student", port=3306)
    c = database.cursor()


    c.execute("select team from accounts where username='{}'".format(session['username']))

    data = c.fetchone()
    for i in data:

        if i == 'yes':
            t = database.cursor()
            t.execute("select teamname from accounts where username='{}'".format(session['username']))
            team_name=t.fetchone()

            for i in team_name:
                session['teamname']=i
                t.execute("select project from team_manage where teamname='{}'".format(i))
                project=t.fetchone()

                t.execute("select teamcode from team_manage where teamname='{}'".format(i))
                teamcode=t.fetchone()

                t.execute("select team_members,roll_no,branch from {}".format(i))
                data = t.fetchall()


            return render_template('team_table.html',table=data,project=project,teamcode=teamcode)

    return render_template('no_team.html')

@app.route('/homepage/submit',methods=['POST','GET'])
def submit():
    if request.method=='POST':
        database = MySQLdb.connect(host="185.28.21.1", user="u320202036_mentor", password="Conzura9346@", database="u320202036_mentor", port=3306)
        c=database.cursor()
        file1=request.form['ffname']












        def insertBLOB( name, photo):
            print("Inserting BLOB into project_files table")
            try:




                connection = MySQLdb.connect(host="185.28.21.1", user="u320202036_mentor", password="Conzura9346@", database="u320202036_mentor", port=3306)
                cursor = connection.cursor()
                sql_insert_blob_query = """ INSERT INTO project_files
                                  ( name, file,teamname,file_name) VALUES (%s,%s,%s,%s)"""
                conn =MySQLdb.connect(host="185.28.21.1", user="u320202036_student", password="Conzura9346@", database="u320202036_student", port=3306)
                cur=conn.cursor()

                cur.execute("select teamname from accounts where username='{}'".format(session['username']))
                team_name=cur.fetchone()

                for tt in team_name:

                    #empPicture = convertToBinaryData(photo)
                    # file = convertToBinaryData(biodataFile)

                    # Convert data into tuple format
                    insert_blob_tuple = (name, photo,tt,photo)
                    result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
                    connection.commit()
                    print("Image and file inserted successfully as a BLOB into python_employee table", result)
#######################################################################
                    cursor5 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

                    conn = MySQLdb.connect(host="185.28.21.1", user="u320202036_mentor", password="Conzura9346@",
                                           database="u320202036_mentor", port=3306)

                    cur = conn.cursor()

                    # cur.execute("update project_files set download='yes' where teamname='{}'".format(i))
                    cur.execute("select id from project_files where teamname='{}'".format(tt))
                    id = cur.fetchone()

                    for i in id:
                        cur.execute("select file_name from project_files where id='{}'".format(i))
                        filename = cur.fetchone()
                        conn.commit()

                        for i in filename:
                            print(str(i)[1:])

                            url = storage.child('images').child(str(i)[:]).get_url(None)
                            print(url)
                    return render_template('proj_already.html', link=url)

            except ArithmeticError as error:
                print("Failed inserting BLOB data into MySQL table {}".format(error))

        insertBLOB( session['username'], file1)

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select teamname from accounts where username='{}'".format(session['username']))
        teamname=cursor.fetchone()
        for i in teamname:

            cursor.execute("update team_manage set proj_sub='yes' where teamname={}".format(i))





            mysql.connection.commit()

            return render_template('proj_already.html')

    return render_template('suzz.html',msg="cant submit details")
#####################################################################################################################
@app.route('/homepage/team_view/team',methods=['POST','GET'])
def team():


    if request.method=='POST' and  'teamname' in request.form and 'teamcode' in request.form and 'project' in request.form:
        name = session['username']
        teamname=request.form['teamname']
        teamname=str(teamname).replace(" ","")
        teamcode=request.form['teamcode']
        project=request.form['project']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select roll_no from accounts where username='{}'".format(session['username']))
        r=cursor.fetchone()
        cursor.execute("select branch from accounts where username='{}'".format(session['username']))
        b=cursor.fetchone()
        cursor.execute("create table {}(team_members varchar(30),project varchar(50),roll_no varchar(50),branch varchar(50))".format(teamname))
        cursor.execute("insert into {}(team_members,project,roll_no,branch) values('{}','{}','{}','{}')".format(teamname,session['username'],project,r['roll_no'],b['branch']))

        cursor.execute("update accounts set teamname='{}' where username='{}';".format(teamname,session['username']))
        cursor.execute("update accounts set team='yes' where username='{}'".format(session['username']))
        cursor.execute("insert into team_manage(teamname,project,teamcode,mentor) values('{}','{}','{}','None')".format(teamname,project,teamcode))
        mysql.connection.commit()
        session['teamname']=teamname
        return render_template('team_table.html')

    else:
        return render_template('no_team.html')
@app.route('/homepage/project')
def project():
    database =MySQLdb.connect(host="185.28.21.1", user="u320202036_student", password="Conzura9346@", database="u320202036_student", port=3306)
    c = database.cursor()
    c.execute("select teamname from accounts where username='{}'".format(session['username']))
    d=c.fetchone()

    for i in d:
        if i != None:
            c.execute("select mentor from team_manage where teamname='{}'".format(i))
            mentor = c.fetchone()
            for i in mentor:
                if i == 'None':
                    return render_template('no_mentor.html')


    for t in d:
        if t!=None:
            c.execute("select marks from team_manage where teamname='{}'".format(t))
            marks=c.fetchone()
            print(marks)
            for mark in marks:
                if mark!=None:
                    db = MySQLdb.connect(host="185.28.21.1", user="u320202036_student", password="Conzura9346@", database="u320202036_student", port=3306)
                    cur = db.cursor()
                    cur.execute("select mentor from team_manage where teamname='{}'".format(t))
                    mentor=cur.fetchone()
                    dba = MySQLdb.connect(host="185.28.21.1", user="u320202036_mentor", password="Conzura9346@", database="u320202036_mentor", port=3306)
                    cura = dba.cursor()
                    print(t)
                    cura.execute("select remarks from project_files where teamname='{}'".format(t))
                    global remarks
                    remarks=cura.fetchone()
                    print(remarks)
                    for men in mentor:
                        return render_template("marks.html",marks=mark,mentor=men,link=remarks)
                if mark==None:
                    c.execute("select proj_sub from team_manage where teamname='{}'".format(t))
                    proj_sub = c.fetchone()
                    for i in proj_sub:
                        if i != None:
                            return render_template('proj_already.html')
                        if i == None:
                            return render_template('project.html')
                    return render_template("proj_already.html")



        #
    return render_template("index.html",username=session['username'])

@app.route('/remarks_mentor',methods=['POST','GET'])
def remarks_mentor():
    if request.method=='POST':
        dba =MySQLdb.connect(host="185.28.21.1", user="u320202036_student", password="Conzura9346@", database="u320202036_student", port=3306)
        cura = dba.cursor()
        cura.execute("select teamname from accounts where username='{}'".format(session['username']))
        teamname=cura.fetchone()
        print(teamname[0])
        db =MySQLdb.connect(host="185.28.21.1", user="u320202036_mentor", password="Conzura9346@", database="u320202036_mentor", port=3306)
        cur = db.cursor()
        cur.execute("select remarks from project_files where teamname='{}'".format(teamname[0]))

        remarks = cur.fetchone()
        print(remarks[0])
        return render_template('remarks.html',marks=remarks[0])


@app.route('/homepage/join_team',methods=['POST','GET'])
def join_team():
    if request.method == "POST" and 'teamname' in request.form:

        teamname=request.form['teamname']
        teamcode=request.form['teamcode']

        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        database = MySQLdb.connect(host="185.28.21.1", user="u320202036_student", password="Conzura9346@", database="u320202036_student", port=3306)
        c = database.cursor()
        c.execute("select project from team_manage where teamname='{}'".format(teamname))
        proj = c.fetchone()



        cursor.execute("select roll_no from accounts where username='{}'".format(session['username']))
        roll_no=cursor.fetchone()
	
        cursor.execute("select branch from accounts where username='{}'".format(session['username']))
        branch=cursor.fetchone()

        cursor.execute("insert into {}(team_members,project,roll_no,branch) values('{}','{}','{}','{}')".format(teamname,session['username'],str(proj[0]),roll_no['roll_no'],branch['branch']))
        cursor.execute("update accounts set team='yes' where username='{}'".format(session['username']))
        cursor.execute("update accounts set teamname='{}' where username='{}'".format(teamname,session['username']))
        cursor.execute("select teamname from accounts where username='{}'".format(session['username']))
        mysql.connection.commit()
        session['teamname']=teamname

        return (team_view())
    return render_template('no_team.html')
@app.route('/account')
def account():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("select email from accounts where username='{}'".format(session['username']))
    email=cursor.fetchone()
    cursor.execute("select roll_no from accounts where username='{}'".format(session['username']))
    roll_no=cursor.fetchone()
    cursor.execute("select branch from accounts where username='{}'".format(session['username']))
    branch=cursor.fetchone()
    return render_template('account.html',branch=branch['branch'],roll_no=roll_no['roll_no'],username=session['username'],email=email["email"])
    #return render_template('account.html')
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
    session.pop('teamname',None)
    return render_template('year.html')



if __name__ == '__main__':
    app.secret_key='success'
    app.debug=True
    app.run()


