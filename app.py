"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.app_context().push()
app.config['SECRET_KEY']="blogly-secret"

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

debug=DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

# ************************************************************
# REDIRECT WILL BE FIXED IN A LATER STEP
# ************************************************************
@app.route('/')
def homepage():
    '''Redirect to list of users'''
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ IN [/]")
    return redirect('/users')

@app.route('/users')
def users_page():
    '''Show all users. Make these links to view the detail page for the user. Have a link here to the add-user form'''
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ IN [/users]")
    all_users = User.query.all()

    return render_template('users.html', all_users=all_users)


@app.route('/users/new')
def newUser():
    '''Show an add form for users'''
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ IN [/users/new]")
    return render_template('create.html')

@app.route('/users/new', methods=['POST'])
def do_newUser():
    '''Process the add form, adding a new user and going back to /users'''
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ IN [/users/new] POST")
    f_name = request.form.get('first')
    l_name = request.form.get('last')
    img_url = request.form.get('image')
    if img_url:
       img_url = img_url
    else:
        img_url = None
    
    newUser = User(first_name=f_name, last_name=l_name, image_url=img_url)
    db.session.add(newUser)
    db.session.commit()
    
    print(User.query.all())
    return redirect('/users')

@app.route('/users/<int:user_id>')
def userDetails(user_id):
    '''Show information about the given user. Have a button to get to their edit page, and to delete the user'''
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ IN [/users/user_id]")
    user = User.query.get_or_404(user_id)
    return render_template('user-page.html', user=user)

@app.route('/users/<int:user_id>/edit')
def editUser(user_id):
    '''Show the edit page for a user. Have a cancel button that returns to the detail page for a user, and a save button that updates the user.'''
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ IN [/users/user_id/edit]")
    user = User.query.get_or_404(user_id)
    return render_template('edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def do_editUser(user_id):
    '''Process the edit form, returning the user to the /users page.'''
    fname = request.form['first']
    lname = request.form['last']
    img = request.form['image']
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ IN [/users/user_id/edit] POST")
    
    user = User.query.get_or_404(user_id)
    user.first_name = fname
    user.last_name = lname
    user.image_url = img
    
    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def do_deleteUser(user_id):
    '''Delete the user.'''
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ IN [/users/user_id/delete]")
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect("/users")