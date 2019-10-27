from flask import render_template, url_for, redirect, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from __init__ import app, bcrypt, db
from forms import RegistrationForm, LoginForm, UpdateAccountForm
from models import User
from utils import save_picture


@app.route('/')
@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    This is the view for registering a user.
    """
    
    form = RegistrationForm()
    
    # if the current user is authenticated then redirected to the home page
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if form.validate_on_submit():
        # encrypt the password using bcrypt
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        if form.picture.data:
            # the save_picture function from the utils module for saving the image in cropped size
            image_file = save_picture(form.picture.data)
            
        # setting the user with the data from the register form.
        user = User(username=form.username.data, email=form.email.data, 
                    password=hashed_password, image_file=image_file)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created', 'sucess')
        return redirect(url_for('home'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    this is the view for siginig in a user
    """
  
    # if the current user is authenticated then redirect to the home page.
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    
    # validating the data from the form with the data from the database.
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() 
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    """
    This is the view for logout
    """
    
    # using the method from the flask module
    logout_user()
    return redirect(url_for('home'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    """
    This is the view for updating the account information of the authenticated user
    """
    
    form = UpdateAccountForm()
    
    # perform actions when the form is submitted
    if form.validate_on_submit():
        # checking if the form contains a picture file
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        # changing the current user details with the form data
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    # performs action if the form method is get
    elif request.method == 'GET':
        # setting the form data with the user data from the database
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)
