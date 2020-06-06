from flask import Flask, render_template, request, flash, redirect, url_for, current_app
from blog import app, db, bycrpt, login_manager
from flask_login import login_user, login_required, current_user, logout_user
from blog.models import User, Post
#these package for handle images from app and db
import os
import secrets

#for save photo to /images folder
def save_images(photo):
   hash_photo = secrets.token_urlsafe(10)
   _, file_extention = os.path.splitext(photo.filename)
   photo_name = hash_photo + file_extention
   file_path = os.path.join(current_app.root_path, 'static/images', photo_name)
   photo.save(file_path)
   return photo_name

#home page
@app.route('/')
def home():
   posts = Post.query.order_by(Post.id.desc()).all()
   return render_template('index.html',posts=posts)

#each post page
@app.route('/post/<int:post_id>/<string:slug>', methods=['POST','GET'])
def post(post_id, slug):
   post = Post.query.get_or_404(post_id)
   posts = Post.query.order_by(Post.id.desc()).all()
   return render_template('image-post.html', post=post,posts=posts)

#user signup
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

#user login
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

#user logout
@app.route('/logout')
@login_required
def logout():
   logout_user()
   return redirect(url_for('login'))

#user dashboard
@app.route('/dashboard')
@login_required
def dashboard():
   posts = Post.query.order_by(Post.id.desc()).all()
   return render_template('admin/dashboard.html', posts=posts)

#user create post
@app.route('/addpost', methods=['POST','GET'])
@login_required
def addpsot():
   if request.method=="POST":
      title = request.form.get('title')
      body = request.form.get('content')
      photo = save_images(request.files.get('photo'))

      post = Post(title=title,body=body,image=photo,author=current_user)
      db.session.add(post)
      db.session.commit()
      flash('Your post has been submited', 'success')
      return redirect('dashboard')
   return render_template('admin/addpost.html')

#user update post
@app.route('/updatepost/<id>', methods=['POST','GET'])
@login_required
def updatepost(id):
   post =Post.query.get_or_404(id)
   if request.method=="POST":
      post.title = request.form.get('title')
      post.body = request.form.get('content')
      db.session.commit()
      flash('post updated', 'success')
      return redirect(url_for('dashboard'))
   return render_template('admin/updatepost.html', post=post)