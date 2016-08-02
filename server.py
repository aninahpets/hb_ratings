"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask_debugtoolbar import DebugToolbarExtension
from flask import (Flask, render_template, redirect, request, flash,
                   session)

from model import User, Rating, Movie, connect_to_db, db
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/users')
def user_list():
    """List of users."""
    users = User.query.all()

    return render_template("user_list.html", users=users)

@app.route('/login')
def login():
    """Login Page"""

    return render_template("login.html")    


@app.route('/submit', methods=['POST']) 
def submit():
    """Page after login submission"""
    
    #get email and password from the login.html form
    email = request.form.get('email')
    password = request.form.get('password')

    #get user object with the matching email from form
    user = User.query.filter_by(email=email).all()

    if user == []:
        #add to db
        users.insert().

    else:
        #if statement to validate password
        if user.password == password:
            flash('You have successfully logged in.')
            user.user_id = session[user_id]
        else:
            flash('You have NOT successfully logged in.')

    return redirect('/') 


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
