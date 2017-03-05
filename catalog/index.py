from flask import Flask, render_template, request, redirect, jsonify, url_for, flash  # NOQA
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Item
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(open('g_client_secrets.json', 'r').read())['web']['client_id']  # NOQA
APPLICATION_NAME = "Catalog App"

# Connect to Database and create database session
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Route Handlers


# User Auth
@app.route("/login")
def showLogin():
    # Create anti-forgery state token
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))  # NOQA
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# Handler for Facebook OAuth logic
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    # strip expire tag from access token
    token = result.split("&")[0]


    url = 'https://graph.facebook.com/v2.8/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout, let's strip out the information before the equals sign in our token
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = 'https://graph.facebook.com/v2.8/me/picture?%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output

@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must be included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id,access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


# Route handler for Google OAuth logic
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code, now compatible with Python3
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('g_client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    # Submit request, parse response - Python3 compatible
    h = httplib2.Http()
    response = h.request(url, 'GET')[1]
    str_response = response.decode('utf-8')
    result = json.loads(str_response)

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()
    
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    return output
    
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] != '200':
        # For whatever reason, the given token was invalid.
        response = make_response(json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response
        
# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            # del login_session['credentials']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out!")
        return redirect(url_for('showCategories'))
    else:
        flash("You were not logged in!")
        return redirect(url_for('showCategories'))

# User Helper Functions
def createUser(login_session):
    """
    This function accepts the login_session as the only parameter,
    the username and email stored in the login_session are used
    to create a new user into the database.
    
    The function will return the user's id of newly created user.
    """
    newUser = User(name=login_session['username'],
                   email=login_session['email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    """
    This function accepts the a user_id, and will return the
    corresponding user object.
    """
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    """
    This function accepts email as the parameter, and will
    return the corresponding user's id of that email, if user exists.
    """
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

def checkOwnership(obj, login_session):
    """
    This function helps to check if the current logged in user
    is the creator of the given category or a given item.
    
    This function return True if the current user owns the category,
    otherwise, it will return False.
    """
    # the user has logged in at this moment
    userID = getUserID(login_session["email"])
    # comparing user_id is a better approach
    # Because different user still can have same usernames
    if obj.user_id == userID:
        return True
    else:
        return False


@app.route("/")
def home():
    return redirect(url_for("showCategories"))


# Catagory CRUD
@app.route("/categories")
def showCategories():
    categories = session.query(Category).order_by(Category.name)
    return render_template("categories.html",
                           categories=categories,
                           login_session=login_session)
    
@app.route("/categories/<int:category_id>")
def showCategory(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    return render_template("category.html",
                           category=category,
                           items=items,
                           login_session=login_session)
    
@app.route("/categories/new", methods=['GET', 'POST'])
def newCategory():
    error = {}
    if "username" not in login_session:
        # if no user logged in, we redirect to login page
        flash("Please login first")
        return redirect(url_for("showLogin"))
    
    # At this point, user has logged in, we can proceed
    if request.method == "POST":
        # handerl for the POST request
        has_error = False
        category_name = request.form['category_name']
        category_imgurl = request.form['category_imgurl']
        if not category_name:
            has_error = True
            error['name_error'] = "Category name cannot be empty!"
        if not category_imgurl:
            has_error = True
            error['imgurl_error'] = 'Category imgurl cannot be empty!'
        if has_error:
            return render_template("newcategory.html",
                                   error=error,
                                   category_name=category_name,
                                   category_imgurl=category_imgurl,
                                   login_session=login_session)
        else:
            # Now that user has valid input we will create the category
            new_category = Category(user_id=getUserID(login_session["email"]),
                                    name=category_name,
                                    imgurl=category_imgurl,
                                    creator=login_session["username"])
            session.add(new_category)
            session.commit()
            flash("New category %s successfully added!" % new_category.name)
            return redirect(url_for("showCategories"))

    else:
        # handler for the GET request, render the form
        return render_template("newcategory.html",
                               error=error,
                               login_session=login_session)
    
@app.route("/categories/<int:category_id>/edit", methods=['GET', 'POST'])
def editCategory(category_id):
    error = {}
    category = session.query(Category).filter_by(id=category_id).one()
    
    if "username" not in login_session:
        # If not logged in, let user login frist
        flash("Please login first!")
        return redirect(url_for("showLogin"))
        
    if not checkOwnership(category, login_session):
        # We redirect to the homepage, if current user doesn't own the category
        flash("Sorry, you cannot edit other's category!")
        return redirect(url_for("showCategory", category_id=category_id))
    
    # At this point, user owns the category, we can proceed
    if request.method == 'POST':
        # handler for the POST request
        has_error = False
        category_name = request.form['category_name']
        category_imgurl = request.form['category_imgurl']
        if not category_name:
            has_error = True
            error['name_error'] = "Category name cannot be empty!"
        if not category_imgurl:
            has_error = True
            error['imgurl_error'] = 'Category imgurl cannot be empty!'
        if has_error:
            return render_template("editcategory.html",
                                   error=error,
                                   category=category,
                                   login_session=login_session)
        else:
            # User's input is valid, we allow this update
            category.name = category_name
            category.imgurl = category_imgurl
            session.add(category)
            session.commit()
            flash("Category %s successfully updated!" % category.name)
            return redirect(url_for("showCategory",
                                    category_id=category_id))
    else:
        # handler for the GET request, we render the form
        return render_template("editcategory.html",
                               error=error,
                               category=category,
                               login_session=login_session)
    
@app.route("/categories/<int:category_id>/delete", methods=["GET", "POST"])
def deleteCategory(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    if "username" not in login_session:
        # If not logged in, let user login frist
        flash("Please login first!")
        return redirect(url_for("showLogin"))
        
    if not checkOwnership(category, login_session):
        # We redirect to the homepage, if current user doesn't own the category
        flash("Sorry, you cannot delete other's category!")
        return redirect(url_for("showCategory", category_id=category_id))

    # At this point, the user owns the given category, we can proceed
    if request.method == "POST":
        # handler for the post request
        session.delete(category)
        session.commit()
        flash("Category %s successfully deleted!" % category.name)
        return redirect(url_for("showCategories"))
    else:
        # handler for the get request, render the confirmation form
        return render_template("deletecategory.html",
                               category=category,
                               login_session=login_session)
    
# Item CRUD
@app.route("/categories/<int:category_id>/items/<int:item_id>")
def showItem(category_id, item_id):
    item = session.query(Item).filter_by(category_id=category_id, id=item_id).one()
    return render_template("item.html",
                           item=item,
                           login_session=login_session)
    
    
@app.route("/categories/<int:category_id>/items/new", methods=['GET', 'POST'])
def newItem(category_id):
    error = {}
    category = session.query(Category).filter_by(id=category_id).one()
    if "username" not in login_session:
        # If not logged in, let user login frist
        flash("Please login first!")
        return redirect(url_for("showLogin"))
    
    # At this point, user has logged in, we can proceed
    if request.method == 'POST':
        # handler for the post request
        has_error = False
        item_name = request.form['item_name']
        item_imgurl = request.form['item_imgurl']
        item_desp = request.form['item_desp']
        if not item_name:
            has_error = True
            error['name_error'] = "Item name cannot be empty!"
        if not item_imgurl:
            has_error = True
            error['imgurl_error'] = "Item imgurl cannot be empty!"
        if not item_desp:
            has_error = True
            error['desp_error'] = "Item description cannot be empty!"
        if has_error:
            return render_template("newitem.html",
                                   error=error,
                                   category=category,
                                   item_name=item_name,
                                   item_imgurl=item_imgurl,
                                   item_desp=item_desp,
                                   login_session=login_session)
        else:
            # user's input is valid, we allow creating this item
            newitem = Item(user_id=getUserID(login_session["email"]),
                           category=category,
                           name=item_name,
                           imgurl=item_imgurl,
                           description=item_desp,
                           creator=login_session["username"])
            session.add(newitem)
            session.commit()
            flash("New item %s of category %s successfully created!" % (category.name, newitem.name))
            return redirect(url_for("showCategory", category_id=category.id))
    else:
        # handler for the get reuqest, we render the form of adding new item
        return render_template("newitem.html",
                               error=error,
                               category=category,
                               login_session=login_session)
    
@app.route("/categories/<int:category_id>/items/<int:item_id>/edit", methods=['GET', 'POST'])
def editItem(category_id, item_id):
    error = {}
    category = session.query(Category).filter_by(id=category_id).one()
    item = session.query(Item).filter_by(id=item_id).one()

    if "username" not in login_session:
        # if no user logged in, we redirect to login page
        flash("Please login first")
        return redirect(url_for("showLogin"))
        
    if not checkOwnership(item, login_session):
        # if the user doesn't own the item, redirect to showItem page
        flash("Sorry, you cannot edit other's item")
        return redirect(url_for("showItem",
                                category_id=category.id,
                                item_id=item.id))
    
    if request.method == "POST":
        has_error = False
        item_name = request.form['item_name']
        item_imgurl = request.form['item_imgurl']
        item_desp = request.form['item_desp']
        if not item_name:
            has_error = True
            error['name_error'] = "Item name cannot be empty!"
        if not item_imgurl:
            has_error = True
            error['imgurl_error'] = "Item imgurl cannot be empty!"
        if not item_desp:
            has_error = True
            error['desp_error'] = "Item description cannot be empty!"
        if has_error:
            return render_template("edititem.html",
                                   error=error,
                                   category=category,
                                   item=item,
                                   login_session=login_session)
        else:
            # user's input is valid, everything is fine
            # we allow updating this item
            item.name = item_name
            item.imgurl = item_imgurl
            item.description = item_desp
            session.add(item)
            session.commit()
            flash("Item %s of category %s successfully updated!" % (item.name, category.name))  # NOQA
            return redirect(url_for("showItem",
                                    category_id=category.id,
                                    item_id=item.id))
    else:
        # handler for the get request, we render the form of editing item
        return render_template("edititem.html",
                               error=error,
                               category=category,
                               item=item,
                               login_session=login_session)

@app.route("/categories/<int:category_id>/items/<int:item_id>/delete", methods=['GET', 'POST'])
def deleteItem(category_id, item_id):
    category = session.query(Category).filter_by(id=category_id).one()
    item = session.query(Item).filter_by(id=item_id).one()
    
    if "username" not in login_session:
        # if no user logged in, we redirect to login page
        flash("Please login first")
        return redirect(url_for("showLogin"))
        
    if not checkOwnership(item, login_session):
        # if the user doesn't own the item, redirect to showItem page
        flash("Sorry, you cannot edit other's item")
        return redirect(url_for("showItem",
                                category_id=category.id,
                                item_id=item.id))
    
    if request.method == "POST":
        # Now we actually delete the item from our database
        session.delete(item)
        session.commit()
        flash("Item %s of category %s successfully deleted!" % (item.name, category.name))  # NOQA
        return redirect(url_for("showCategory", category_id=category.id))
    else:
        # handler for the get request
        return render_template("deleteitem.html",
                               category=category,
                               item=item,
                               login_session=login_session)
        
# JSON APIs to view Catalog

# JSON endpoint for showing all the categories
@app.route('/categories/JSON')
def categoriesJSON():
    categories = session.query(Category).order_by(Category.name)
    return jsonify(categories=[c.serialize for c in categories])

# JSON endpoint for showing all items of a given category
@app.route('/categories/<int:category_id>/JSON')
def categoryJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    return jsonify(items=[i.serialize for i in items])


# JSON endpoint for showing information of a given item
@app.route('/categories/<int:category_id>/items/<int:item_id>/JSON')
def menuItemJSON(category_id, item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    return jsonify(item=item.serialize)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
