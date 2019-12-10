from flask import Flask,render_template,request,session,redirect
import os
import json
import random
project_dir = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'the-random-string'
from flask_sqlalchemy import SQLAlchemy
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "bookdatabase.db"))
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
with open("config.json",'r') as a:
    parms=json.load(a)["Parms"]

@app.route('/delete/<string:s_no>',methods=["Get","POST"])
def delete(s_no):
    if 'user' in session and session['user'] == parms['username'] and parms['role']=="Admin":
        if request.method == "GET":
            user_found = User.query.filter_by(id=s_no).first()
            db.session.delete(user_found)
            db.session.commit()
            return main()
    elif 'user' in session and session['user'] == parms['username'] and parms['role'] == "Student":
        if request.method == "GET":
            user_found = User.query.filter_by(id=s_no).first()
            db.session.delete(user_found)
            db.session.commit()
            return logout()
    elif 'user' in session and session['user'] == parms['username'] and parms['role'] == "Teacher":
        if request.method == "GET":
            user_found = User.query.filter_by(id=s_no).first()
            print(user_found)
            db.session.delete(user_found)
            db.session.commit()
            return logout()
    return "Admin In NOT Session"

@app.route('/edit/<string:s_no>',methods=["Get","POST"])
def edit(s_no):
    if 'user' in session and session['user'] == parms['username'] and parms['role']=="Admin":
        if request.method == "POST":
            user1 = User.query.filter_by(id=s_no).first()
            user1.uname = request.form['username']
            user1.email = request.form['email']
            db.session.commit()
            return main()
        user = User.query.filter_by(id=s_no).first()
        return render_template("edit.html",parms=parms,s_no=s_no,user=user)
    elif 'user' in session and session['user'] == parms['username'] and parms['role'] == "Student":
        if request.method == "POST":
            user1 = User.query.filter_by(id=s_no).first()
            user1.uname = request.form['username']
            user1.email = request.form['email']
            db.session.commit()
            return main()
        user = User.query.filter_by(id=s_no).first()
        return render_template("edit_st.html",parms=parms,s_no=s_no,user=user)
    elif 'user' in session and session['user'] == parms['username'] and parms['role'] == "Teacher":
        if request.method == "POST":
            user1 = User.query.filter_by(id=s_no).first()
            user1.uname = request.form['username']
            user1.email = request.form['email']
            db.session.commit()
            return main()
        user = User.query.filter_by(id=s_no).first()
        return render_template("edit_st.html",parms=parms,s_no=s_no,user=user)
    return "Admin In NOT Session"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uname = db.Column(db.String(40),unique=False, nullable=False)
    email = db.Column(db.String(40), unique=False, nullable=False)
    password = db.Column(db.String(40),unique=False, nullable=False)
    role = db.Column(db.String(40), unique=False, nullable=False)
# db.create_all()
@app.route('/student',methods=["GET","POST"])
def student():
    if 'user' in session and session['user'] == parms['username'] and parms['role'] == "Admin":
        user_found=User.query.filter_by(role="Student").all()
        return render_template("display.html",parms=parms,user=user_found)
    return "Admin In NOT Session"

@app.route('/display',methods=["GET","POST"])
def display():
    if 'user' in session and session['user'] == parms['username'] and parms['role'] == "Admin":
        user_found=User.query.filter_by(role="Teacher").all()
        return render_template("display.html",parms=parms,user=user_found)
    elif 'user' in session and session['user'] == parms['username'] and parms['role'] == "Student":
        user_found = User.query.filter_by(id=parms['st_id']).all()
        return render_template("display_st.html", parms=parms, user=user_found)
    elif 'user' in session and session['user'] == parms['username'] and parms['role'] == "Teacher":
        user_found = User.query.filter_by(id=parms['st_id']).all()
        return render_template("display_te.html", parms=parms, user=user_found)
    return "Admin In NOT Session"

@app.route('/register',methods=["GET","POST"])
def register():
    if 'user' in session and session['user'] == parms['username'] and parms['role'] == "Admin":
        password = random.randint(1, 10000)
        return render_template("register.html",parms=parms,password=password)
    return "Admin In NOT Session"
@app.route('/logout',methods=["GET","POST"])
def logout():
    if 'user' in session and session['user']==parms['username']:
        session.pop('user')
    return render_template("index.html")

@app.route('/test1', methods=["POST", "GET"])
def test1():
    # print(request.form['username'])
    if 'user' in session and session['user'] == parms['username'] and parms['role'] == "Admin":
        if request.method == "POST":
            user1 = User()
            user1.uname = request.form['username']
            user1.email = request.form['email']
            user1.password = request.form['password']
            user1.role = request.form['role']
            db.session.add(user1)
            db.session.commit()
            password = random.randint(1, 10000)
        return render_template('register.html',parms=parms,password=password)
    return "Admin In NOT Session"

@app.route('/',methods=["GET","POST"])
def main():
    if 'user' in session and session['user']==parms['username'] and parms['role']=="Admin":
        return render_template("layout.html",parms=parms)
    elif 'user' in session and session['user'] == parms['username'] and parms['role'] == "Student":
        return render_template("student_layout.html")
    elif 'user' in session and session['user'] == parms['username'] and parms['role'] == "Teacher":
        return render_template("teacher_layout.html")
    elif request.method=="POST":
        uname=request.form.get("username")
        pas= request.form.get("pass")
        user_found = User.query.filter_by(email=uname,password=pas).first()
        if user_found:
            username=user_found.uname
            parms['username']=uname
            parms['name']=user_found.uname
            session['user']=uname
            parms['role']=user_found.role
            parms['st_id']=user_found.id
            if user_found.role in "Admin":
                return render_template("layout.html",parms=parms)
            elif user_found.role in "Teacher":
                return render_template("teacher_layout.html")
            elif user_found.role in "Student":
                return render_template("student_layout.html")
            else:
                return "Role Not Found"
        render_template("index.html")
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)