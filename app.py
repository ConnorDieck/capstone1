from flask import Flask, request, redirect, render_template, session, flash, g
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized
from sqlalchemy.exc import IntegrityError

from models import db, connect_db, User, Book, Club, Membership, Read, Note
from forms import LoginForm, RegisterForm, NotesForm, DeleteForm

CURR_USER_KEY = "curr_user"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///booktalk' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['SQLALCHEMY_ECHO'] = True

app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

toolbar = DebugToolbarExtension(app)


########################################################################
# User register/login/logout


@app.before_request
def load_user():
    """If logged in, load curr user."""
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id

def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route("/register", methods=["GET", "POST"])
def register():
    """Generate and handles registration submission"""

    if g.user:
        flash("You're already registered", "text-danger")
        return redirect(f"/")

    form = RegisterForm()
    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data
        email = form.email.data
        image = form.image.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        bio = form.bio.data

        user = User.register(username=username, pwd=password, email=email, first=first_name, last=last_name, bio=bio, image=image)

        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Sorry, this username is already taken. Please choose another')
            return render_template('users/register.html', form=form)

        do_login(user)

        flash(f'Your account has been created. Welcome to BookTalk, {user.username}!', "text-success")

        return redirect ("/")
    
    else:
        return render_template('users/register.html', form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Generates and handles login form submission"""
    if g.user:
        flash("You're already logged in.", "text-danger")
        return redirect("/")

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            # flash(f"Welcome Back, {user.first_name}!", "text-primary")
            do_login(user)
            return redirect('/')
        else:
            form.username.errors = ['Invalid username/password.']

    return render_template('users/login.html', form=form)

@app.route("/logout")
def logout():
    """Logs out current user"""

    do_logout()

    return redirect("/login")


###########################################################################
# Home page


@app.route("/")
def show_home():
    """Show home page."""

    # If no user is signed in, redirect to log-in page
    if g.user:
        
        return render_template("home.html", user=g.user)

    else:
        return redirect("/login")


############################################################################
# Clubs routes


@app.route("/clubs")
def show_clubs():
    """Shows list of active clubs"""

    clubs = Club.query.all()

    return render_template("clubs.html", clubs=clubs)

