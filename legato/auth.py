from . import db
from .models import User
from .helpers import apology, validate_password
from .config import salt_password
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    # login page to legato
    if request.method == 'POST':
        # get credentials from user
        email = request.form.get("email")
        password = request.form.get("password")
        # salt the password again so it matches the signup
        salted_pass = salt_password(password)
        # query the db looking for user
        user = User.query.filter_by(email=email).first()
        # if a matching user is found, check whether password is correct
        if user:
            if check_password_hash(user.password, salted_pass):
                # if password is correct, log in user and redirect to home page
                flash("Logged in!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.index'))
            else:
                # if password is incorrect, flash an error messag
                flash('Password is incorrect.', category='error')
        else:
            # if email does not exist in database, flash an error message
            flash('Email does not exist.', category='error')
    # if a GET request is received, render the login page
    return render_template("login.html", user=current_user)


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    # signup page, for registering to legato
    if request.method == "POST":
        # get credentials from user
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        # if username input is blank
        if not username:
            return apology("Missing username", 400)
        # if email input is blank
        if not email:
            return apology("Missing email", 400)
        if not password:
            return apology("Missing password", 400)
        if password != confirmation:
            return apology("Passwords don't match", 400)
        # check if passoword matches regex conditions
        if not validate_password(password):
            return apology("Please select a valid password", 400)
            # get an empty list of usernames
        rows = User.query.filter_by(username=username).all()

        if len(rows) != 0:
            return apology("Username is not available", 400)
        # if password input is blank or it doesn't match confirmation, return an apology error message

        if password != confirmation:
            return apology("Passwords don't match", 400)
        else:
            # (if no errors) insert new user into users table
            # salt and hash the password for security
            salted_pass = salt_password(password)
            hashed_pass = generate_password_hash(salted_pass)

            # create a new User object and add it to the database
            new_user = User(email=email, username=username,
                            password=hashed_pass)
            db.session.add(new_user)
            db.session.commit()

            # log in the new user and redirect to home page
            login_user(new_user, remember=True)
            flash('User created!')
            return redirect(url_for('views.index'))
    # if a GET request is received, render the signup page
    return render_template("signup.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    # log out the current user and redirect to home page
    logout_user()
    return redirect(url_for("views.index"))
