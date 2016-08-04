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

@app.route('/logout', methods=['POST'])
def logout():
    """Logs User Out"""

    # checks for and deletes user_id from session; returns message to homepage
    if 'user_id' in session:
        del session['user_id']
        print 'removed session'
        return 'logged_out'
    else:
        return 'not_logged_out'

@app.route('/submit', methods=['POST']) 
def submit():
    """Page after login submission"""
    
    #get email and password from the login.html form
    email = request.form.get('email')
    password = request.form.get('password')

    
    try:
        #try statement to see if user exists in database, limiting results to one
        user = User.query.filter_by(email=email).one()
        user_id = user.user_id
        #delete session user_id if other user logged in
        if 'user_id' in session:
            del session['user_id']
        #creates URL for user_details based on user_id
        url = ('/user-details/%s' % str(user_id))
        # if statement to validate password
        if user.password == password:
            flash('You have successfully logged in.')
            session['user_id'] = user.user_id #add user id to session
            return redirect(url)
        else:
            flash('Your password was incorrect and you were not logged in.')
            return redirect('/') #for incorrect login, send user to homepage

    #except statement to run if query returns error and user does not exist
    except:
        #delete session user_id if other user logged in
        if 'user_id' in session:
            del session['user_id']
        new_user = User(email=email, password=password)
        db.session.add(new_user) #add user to db
        db.session.commit()
        flash('You have successfully created an account.')
        #need to run a new query to get user_id to create session
        new_user_id = db.session.query(User.user_id).filter_by(email=email).one()[0]
        session['user_id'] = new_user_id #add user id to session
        #creates URL for user_details based on user_id
        url = ('/user-details/%s' % str(new_user_id))
        return redirect(url)
 

@app.route('/user-details/<int:user_id>')
def user_details(user_id):
    """Generates user details"""
    # movielist.

    user = db.session.query(User).filter_by(user_id=user_id).one()

    return render_template("user_details.html", user=user)


@app.route('/movies')
def movie_list():
    """List of movies."""
    movies = Movie.query.order_by(Movie.title).all()

    return render_template("movie_list.html", movies=movies)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
