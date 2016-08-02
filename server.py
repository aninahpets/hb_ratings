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

    #get user list with the matching email from form
    user = User.query.filter_by(email=email).all()

    if user == []:
        #add to db
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('You have successfully created an account.')
        #need to run a new query to get user_id to create session
        new_user_id = db.session.query(User.user_id).filter_by(email=email).one()
        session['user_id'] = new_user_id #add user id to session
    else:
        #if statement to validate password
        if user[0].password == password:
            flash('You have successfully logged in.')
            session['user_id'] = user[0].user_id #add user id to session
        else:
            flash('You have NOT successfully logged in.')

    print session
    return redirect('/') 


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
