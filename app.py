"""Blogly application."""

from flask import Flask, render_template, request, session, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "123"
debug = DebugToolbarExtension(app)

app.app_context().push()
connect_db(app)

@app.route('/')
def root():
    """Redirects to list of users."""
    return redirect("/users")

@app.route('/users')
def list_users():
    """Show list of all users in db."""
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/<int:user_id>')
def show_user(user_id):
    """Show details about a single user."""
    user = User.query.get_or_404(user_id)
    return render_template('details.html', user=user)

@app.route('/new_user', methods=["GET"])
def new_user_form():
    "Shows the new user form."
    return render_template('new_user.html')

@app.route('/new_user', methods=["POST"])
def create_user():
    """Handle the new user form."""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"] or None

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>/edit')
def edit_user_form(user_id):
    """Shows the edit user form."""
    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def handle_edit_user_form(user_id):
    """Handle the edit user form."""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"]

    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def handle_delete_user(user_id):
    """Deletes the user."""
    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect("/users")