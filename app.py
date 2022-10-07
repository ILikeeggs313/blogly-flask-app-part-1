"""Blogly application."""

from flask import Flask, render_template, request, session, redirect
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def home_page():
    """Show homepage with the users and links to direct to them"""
    return redirect('/users')

@app.route('/users')
def show_users():
    """Show users"""
    users = User.query.order_by(User.last_name, User.first_name)
    return render_template('users/home.html', users = users)

@app.route('/users/new', methods = ['GET'])
def get_new_form():
    """Show a form to create a new user"""
    return render_template('users/new.html')

@app.route('/users/new', methods = ['POST'])
def post_new_form():
    """post form submission to change the actual database"""
    new_user = User(
        first_name = request.form['first_name'],
        last_name = request.form['last_name'],
        image_url = request.form['image_url'] or None
    )
    db.session.add(new_user)
    db.session.commit()
    #as always, add and commit to change the actual database

    return redirect('/users')
    #to redirect back to users after the form is submitted 
    #and a new user is added

@app.route('/users/<int:user_id>')
def show_users(user_id):
    """Redirect to the page with the users_id, as in the requirement"""
    user = User.query.get_or_404(user_id)
    #wiwll return 404 instead of None if no user exist
    return render_template('users/show.html', user = user)

#new route to handle form submission to update an existing user
@app.route('/users/<int:user_id>/edit', methods = ['POST'])
def users_update(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()
    return redirect ('/users')

#make a new route to handle deleting a user
@app.route('/users/<int:user_id>/delete', methods = ['POST'])
def delete_user(user_id):
    """Handle button submission to delete a user."""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')

