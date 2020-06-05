from flask import Flask, render_template, request, flash, redirect, url_for
from blog import app, db, bycrpt, login_manager
from flask_login import login_user, login_required, current_user, logout_user
from blog.models import User

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
   #If request is 'POST' the Flask will be check user cred from mysql
   if request.method=="POST":
      user = User.query.filter_by(username=request.form.get('username')).first()
      if user:
         flash("The user name already exit", 'warning')
         return redirect(url_for('register'))
      email = User.query.filter_by(email=request.form.get('email')).first()
      if email:
         flash("The email already exit", 'warning')
         return redirect(url_for('register'))
      name = request.form.get('name')
      username = request.form.get('username')
      email = request.form.get('email')
      password = request.form.get('password')
      confirm_password = request.form.get('confirm_password')

      if password != confirm_password:
         flash("Password do not match. Please check and try again", 'warning')
         return redirect(url_for('register'))
      #Encrypt password and send to mysql
      password_has = bycrpt.generate_password_hash(password)

      users = User(name=name, username=username, email=email, password=password_has)
      db.session.add(users)
      db.session.commit()
      flash("Thanks for your registration", 'success')
      return redirect(url_for("dashboard"))


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
   if request.method=="POST":
      # Login and validate the user.
      # user should be an instance of your `User` class
      user = User.query.filter_by(username=request.form.get('username')).first()
      if user and bycrpt.check_password_hash(user.password, request.form.get('password')):
         login_user(user)

         flash('Logged in successfully.', 'success')

         next = request.args.get('next')
      # is_safe_url should check if the url is safe for redirects.
      # See http://flask.pocoo.org/snippets/62/ for an example
         return redirect(next or url_for('dashboard'))

      flash('Wrong password please try again', 'danger')
   return render_template('admin/login.html')


@app.route('/logout')
@login_required
def logout():
   logout_user()
   return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
   return render_template('admin/dashboard.html')
