
from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from flask_login import UserMixin
from flask import render_template,redirect,url_for,flash
from flask_login import login_user


db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///result.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ccd90674f5e2f9064c87d542'
db.init_app(app)
app.app_context().push()

bcrypt = Bcrypt(app)
login_mgr = LoginManager(app)

@login_mgr.user_loader
def load_user(user_id):
    return UserInfo.get(int(user_id))

class UserInfo(db.Model,UserMixin):

    sno = db.Column(db.Integer,nullable = False,primary_key = True)
    username = db.Column(db.String,nullable = False,unique= True)
    password_hash =  db.Column(db.String(length = 60),nullable = False)

    @property
    def password(self):
        return self.password
    @password.setter
    def password(self,plane_text):
        self.password_hash = bcrypt.generate_password_hash(plane_text).decode('utf-8')
                 


    def check_pass(self,attemPass):
        return bcrypt.check_password_hash(self.password_hash,attemPass)

    def __repr__(self) -> str:
        return f'{self.sno} {self.username}'

class Card(db.Model):
    sno = db.Column(db.Integer,nullable = False,primary_key = True)
    item = db.Column(db.String,nullable = False)

    first = db.Column(db.String,nullable = False)
    first_dep = db.Column(db.String,nullable = False)
    first_grp = db.Column(db.String,nullable = False)

    sec = db.Column(db.String,nullable = False)
    sec_dep = db.Column(db.String,nullable = False)
    sec_grp = db.Column(db.String,nullable = False)
    
    third = db.Column(db.String,nullable = False)
    third_dep = db.Column(db.String,nullable = False)
    third_grp = db.Column(db.String,nullable = False)

    def __repr__(self) -> str:
        return f'{self.sno} {self.first}'



class RegisterForm(FlaskForm):
    username = StringField()
    password = PasswordField()
    submit = SubmitField(label='Submit')

class LoginForm(FlaskForm):
    username = StringField()
    password = PasswordField()
    submit = SubmitField(label='Submit')




# @app.route('/register',methods = ['GET','POST'])
# def register():

#     form = RegisterForm()
#     if form.validate_on_submit():
#         user_create = UserInfo(username = form.username.data,password_hash = form.password.data)
#         db.session.add(user_create)
#         db.session.commit()
#         return redirect('/')
#     if form.errors != {}:
#         for err in form.values():
#             flash(f'ERROR: {err}')
    
#     return render_template('register.html',form = form)

@app.route('/Jalakadmin3',methods = ['GET','POST'])
def admin():
    if request.method == 'POST':
        item = request.form['item']

        first = request.form['first']
        first_dep = request.form['first-dep']
        first_grp= request.form['first-grp']

        sec = request.form['sec']
        sec_dep = request.form['sec-dep']
        sec_grp = request.form['sec-grp']
        third = request.form['third']
        third_dep = request.form['third-dep']
        third_grp = request.form['third-grp']

        result_data = Card(item = item,
                            first = first,
                            first_dep = first_dep,
                            first_grp = first_grp,
                            sec = sec,
                            sec_dep = sec_dep,
                            sec_grp = sec_grp,
                            third = third,
                            third_dep = third_dep,
                            third_grp = third_grp)
        db.session.add(result_data)
        db.session.commit()

    all_result = Card.query.all()
    return render_template('admin.html',all_result = all_result)

@app.route('/home')
@app.route('/')
def home():

    all_result = Card.query.all()

    return render_template('index.html',all_result = all_result)

@app.route('/delete/<int:sno>')
def delete(sno):
    record = Card.query.filter_by(sno = sno).first()
    db.session.delete(record)
    db.session.commit()
    return redirect('/Jalakadmin3')
@app.route('/update/<int:sno>', methods = ['GET','POST'])
def update(sno):
    if request.method == 'POST':
        item = request.form['item']

        first = request.form['first']
        first_dep = request.form['first-dep']
        first_grp= request.form['first-grp']

        sec = request.form['sec']
        sec_dep = request.form['sec-dep']
        sec_grp = request.form['sec-grp']
        third = request.form['third']
        third_dep = request.form['third-dep']
        third_grp = request.form['third-grp']
        result_data = Card.query.filter_by(sno=sno).first()

        result_data.item = item

        result_data.first = first
        result_data.first_dep = first_dep
        result_data.first_grp = first_grp
        
        result_data.sec = sec
        result_data.sec_dep = sec_dep
        result_data.sec_grp = sec_grp

        result_data.third = third
        result_data.third_dep = third_dep
        result_data.third_grp = third_grp

        db.session.add(result_data)
        db.session.commit()
        return redirect('/Jalakadmin3')


    edit_result = Card.query.filter_by(sno=sno)

    return render_template('update.html',edit_result = edit_result)





# @app.route('/login',methods = ['GET','POST'])
# def login():
    
#     if request.method == 'POST':
#         attempted_user = UserInfo.query.filter_by(username = request.form['username']).first()
        
#         if attempted_user.check_pass(attemPass= request.form[ 'password']):

#             print('logged')
#             flash(f'Successfully Logged in as{attempted_user.username}')
#             return redirect(url_for('admin'))
#         else:
#             print('error')
#             flash('Did not Match!! Try again..',category='danger')
        
#     return render_template('login.html')



if __name__ == '__main__':
    app.run(debug=True,port=5000)