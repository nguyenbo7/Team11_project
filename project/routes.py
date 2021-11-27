from project import myapp_obj
from project.forms import LoginForm
from flask import render_template, flash, redirect

from project import db
from project.models import User, Post
from flask_login import current_user, login_user, logout_user, login_required

@myapp_obj.route("/loggedin")
@login_required
def log():
    return 'Hi you are logged in'

@myapp_obj.route("/logout")
def logout():
    logout_user()
    return redirect('/')

@myapp_obj.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Login invalid username or password!')
            return redirect('/login')
        login_user(user, remember=form.remember_me.data)
        flash(f'Login requested for user {form.username.data},remember_me={form.remember_me.data}')
        flash(f'Login password {form.password.data}')
        return redirect('/')
    return render_template("login.html", form=form)

@myapp_obj.route("/members/<string:name>/")
def getMember(name):
    return 'Hi ' + name

@myapp_obj.route("/signup", methods=['GET','POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
	flash(f'Welcome!')
	username = form.username.data
	email = form.email.data
	password = form.password.data
	user = User(username, email)
	db.session.add(user)
	db.session.commit()
	return redirect("/login")
    return render_templates('signup.html', form=form)

@myapp_obj.route("/home", methods=['GET', 'POST']
def home():
    return render_template('home.html')
