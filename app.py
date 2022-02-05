import os
import requests

from flask import Flask, render_template, redirect, request, flash, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from models import db, connect_db, User, Dish, Cuisine, Meal
from forms import SignupForm, LoginForm, AddMealForm

CURR_USER_KEY = 'curr_user'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (os.environ.get('DATABASE_URL', 'postgresql:///capstone_one'))


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'shhh secret!')

toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def homepage():
    '''Show homepage.'''

    response = requests.get('https://api.edamam.com/api/recipes/v2?type=public', 
        params={
            'term': 'seafood',
            'app_key': 'ccb5ad1a079a4045adc90a739f7f2785',
            'app_id': 'd097d304',
            'limit': 7
        }
    )

    return render_template('homepage.html', meal=response)


# ------- User signup, login, and logout ------- #

@app.before_request
def add_user_to_g():
    '''After logged in, add curr user to Flask global.'''

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    '''Login user.'''

    session[CURR_USER_KEY] = user.id


def do_logout():
    '''Logout user.'''

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    '''Handel user signup.'''

    form = SignupForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data,
            )
            db.session.commit()

        except IntegrityError:
            flash('Username already taken', 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect('/')

    else:
        return render_template('users/signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    '''Handle user login.'''

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            do_login(user)
            flash(f'Welcome back! {user.username}!', 'success')
            return redirect('/')
        
        flash('Invalid username or password', 'danger')

    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout():
    '''Handle user logout.'''

    do_logout()

    flash('You have logged out successfully.', 'secondary')

    return redirect('/login')


# ------- Users route ------- #

@app.route('/users/<int:user_id>')
def show_profile(user_id):
    '''Show user profile.'''

    if not g.user:
        flash('Access unauthorized', 'danger')
        return redirect('/')

    user = User.query.get_or_404(user_id)

    return render_template('users/profile.html', user=user)


@app.route('/users/<int:user_id>/add-meal', methods=['GET', 'POST'])
def add_meal(user_id):
    '''Add a new meal.'''

    if not g.user:
        flash('Access unauthorized', 'danger')
        return redirect('/')

    user = g.user
    form = AddMealForm(obj=user)
    user = User.query.get_or_404(user_id)

    if form.validate_on_submit():
        title = form.title.data
        meal_image = form.meal_image.data
        dish_type = form.dish_type.data
        cuisine_type = form.cuisine_type.data
        recipe = form.recipe.data
        meal = Meal(title=title, meal_image=meal_image, dish_type=dish_type, cuisine_type=cuisine_type, recipe=recipe)

        g.user.meals.append(meal)
        db.session.commit()

        return redirect(f'/users/{user.id}')

    return render_template('meals/new.html', form=form, user=user)





# ------- Meals route ------- #

# @app.route('meals/<uri>')
# def show_meal_details(url):
#     '''Show meal details.'''

