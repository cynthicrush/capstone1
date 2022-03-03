import os
import requests

from flask import Flask, render_template, redirect, request, flash, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from models import db, connect_db, User, Recipe, Likes
from forms import SignupForm, LoginForm, AddRecipeForm

import pdb

CURR_USER_KEY = 'curr_user'
CURR_SEARCH_REQUEST = 'curr_query'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (os.environ.get('DATABASE_URL', 'postgresql:///capstone_one'))


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'shhh secret!')

# toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


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

@app.route('/users/<int:user_id>/recipes')
def show_recipes(user_id):
    '''Show user's recipes.'''

    if not g.user:
        flash('Access unauthorized', 'danger')
        return redirect('/')

    user = User.query.get_or_404(user_id)
    recipes = Recipe.query.filter(Recipe.user_id == user_id).all()

    return render_template('users/recipes.html', user=user, recipes=recipes)


@app.route('/users/<int:user_id>/likes')
def show_likes(user_id):
    '''Show user's likes.'''

    if not g.user:
        flash('Access unauthorized', 'danger')
        return redirect('/')

    user = User.query.get_or_404(user_id)
    likes = Likes.query.filter(Likes.user_id == user_id).all()

    liked_recipe_ids = [recipe.id for recipe in g.user.likes]

    return render_template('users/likes.html', user=user, likes=likes, liked=liked_recipe_ids)


@app.route('/users/add_like/<int:recipe_id>', methods=['POST'])
def add_like(recipe_id):
    '''Like a recipe.'''

    if not g.user:
        flash('Access unauthorized', 'danger')
        return redirect('/')

    current_recipe = Recipe.query.get_or_404(recipe_id)
    if current_recipe.user_id == g.user.id:
        flash('Sorry! You are not allowed to like your own recipes.', 'warning')
        return redirect('/')

    user_likes = g.user.likes

    if current_recipe in user_likes:
        g.user.likes = [like for like in user_likes if like != current_recipe]
    else:
        g.user.likes.append(current_recipe)
    
    db.session.commit()

    return redirect('/')


@app.route('/users/unlike/<int:recipe_id>', methods=['POST'])
def unlike(recipe_id):
    '''Unlike a recipe.'''

    if not g.user:
        flash('Access unauthorized', 'danger')
        return redirect('/')

    current_recipe = Recipe.query.get_or_404(recipe_id)
    if current_recipe.user_id == g.user.id:
        flash('Sorry! You are not allowed to like your own recipes.', 'warning')
        return redirect('/')

    user_likes = g.user.likes

    if current_recipe in user_likes:
        g.user.likes = [like for like in user_likes if like != current_recipe]
    else:
        g.user.likes.append(current_recipe)
    
    db.session.commit()

    return redirect(f'/users/{g.user.id}/likes')

# ---------- Solution 1
# @app.route('/users/search', methods=['GET', 'POST'])
# def search():
#     '''Search all the recipes in the website.'''

#     if not g.user:
#         flash('Access unauthorized', 'danger')
#         return redirect('/')

#     recipes = []

#     if request.method == 'POST':
#         if request.form:
#             search_term = request.form.get('query')
#             session[CURR_SEARCH_REQUEST] = search_term
#         else:
#             search_term = session[CURR_SEARCH_REQUEST]
#         search_term = request.form.get('query')
#         response = requests.get(f'https://api.edamam.com/api/recipes/v2?type=public&q={search_term}&app_id=d097d304&app_key=ccb5ad1a079a4045adc90a739f7f2785')
#         results = response.json()

#         sample_user = User.query.get(1)

#         for recipe in results['hits']:
#             new_dict = {k: v for k, v in recipe['recipe'].items() if k in {'label', 'image',  'ingredientLines', 'cuisineType', 'dishType', 'url'}}
#             url = new_dict['url']
#             # existing_recipe = Recipe.query.filter(Recipe.url==url).all()
#             existing_recipes = Recipe.query.all()
#             for existing_recipe in existing_recipes:
#                 if existing_recipe and len(existing_recipe) > 0:
#                     sample_user.recipes.append(existing_recipe)
#                 else:
#                     new_recipe = Recipe(
#                         title=new_dict['label'], 
#                         recipe_image=new_dict['image'], 
#                         url=new_dict['url'], 
#                         recipe=new_dict['ingredientLines'], 
#                         cuisine_type=new_dict['cuisineType'][0].capitalize(), 
#                         dish_type=new_dict.get('dishType', ['none'])[0].capitalize()
#                     )
                                    
#                     sample_user.recipes.append(new_recipe)
#             recipes.append(new_recipe)
#         db.session.commit()
    
#     return render_template('users/search.html', recipes=recipes)



# ---------- Solution 2
@app.route('/users/search', methods=['GET', 'POST'])
def search():
    '''Search all the recipes in the website.'''

    if not g.user:
        flash('Access unauthorized', 'danger')
        return redirect('/')

    recipes_list = []

    if request.method == 'POST':

        if request.form:
            search_term = request.form.get('query')
            session[CURR_SEARCH_REQUEST] = search_term
        else:
            search_term = session[CURR_SEARCH_REQUEST]
        
        response = requests.get(f'https://api.edamam.com/api/recipes/v2?type=public&q={search_term}&app_id=d097d304&app_key=ccb5ad1a079a4045adc90a739f7f2785')
        results = response.json()

        sample_user = User.query.get(1)
        # print(results)         

        for recipe in results['hits']:
            new_dict = {k: v for k, v in recipe['recipe'].items() if k in {'label', 'image',  'ingredientLines', 'cuisineType', 'dishType', 'url'}}
            
            url = new_dict['url']
            existing_recipe = Recipe.query.filter_by(url=url).first()
            if existing_recipe:
                recipes_list.append(existing_recipe)
            else:
                # pdb.set_trace()
                new_recipe = Recipe(
                title=new_dict['label'], 
                recipe_image=new_dict['image'], 
                url=new_dict['url'], 
                recipe=new_dict['ingredientLines'], 
                cuisine_type=new_dict['cuisineType'][0].capitalize(), 
                dish_type=new_dict.get('dishType', ['none'])[0].capitalize()
                )
                sample_user.recipes.append(new_recipe)

                recipes_list.append(new_recipe)


                
        db.session.commit()
        liked_recipe_ids = [recipe.id for recipe in g.user.likes]
    
    return render_template('users/search.html', recipes=recipes_list, likes=liked_recipe_ids)


# ---------- Original
# @app.route('/users/search', methods=['GET', 'POST'])
# def search():
#     '''Search all the recipes in the website.'''

#     if not g.user:
#         flash('Access unauthorized', 'danger')
#         return redirect('/')

#     recipes = []

#     if request.method == 'POST':

#         response = requests.get(f'https://api.edamam.com/api/recipes/v2?type=public&q={request.form.get("query")}&app_id=d097d304&app_key=ccb5ad1a079a4045adc90a739f7f2785')
#         results = response.json()

#         sample_user = User.query.get(1)
#         # print(results)
#         for recipe in results['hits']:
#             new_dict = {k: v for k, v in recipe['recipe'].items() if k in {'label', 'image',  'ingredientLines', 'cuisineType', 'dishType'}}
#             new_recipe = Recipe(
#                 title=new_dict['label'], 
#                 recipe_image=new_dict['image'], 
#                 recipe=new_dict['ingredientLines'], 
#                 cuisine_type=new_dict['cuisineType'][0].capitalize(), 
#                 dish_type=new_dict.get('dishType', ['none'])[0].capitalize()
#                 # dish_type=new_dict['dishType'][0].capitalize() 
#             )
#             # recipe_data = {
#             #     'title': new_dict['label'], 
#             #     'recipe_image': new_dict['image'], 
#             #     'recipe': new_dict['ingredientLines'], 
#             #     'cuisine_type': new_dict['cuisineType'][0].capitalize(), 
#             #     'dish_type': new_dict.get('dishType', ['None'][0].capitalize())
#             #     # new_dict['dishType'][0].capitalize()
#             # }
#             recipes.append(new_recipe)
#             # new_recipe = Recipe(recipe_data)
#         # db.session.add(new_recipe)
#             sample_user.recipes.append(new_recipe)
#         db.session.commit()

#         # recipes = Recipe.query.all()

    
#     return render_template('users/search.html', recipes=recipes)

@app.route('/users/like/<int:recipe_id>', methods=['POST'])
def like(recipe_id):
    '''Like a recipe.'''

    if not g.user:
        flash('Access unauthorized', 'danger')
        return redirect('/')

    current_recipe = Recipe.query.get_or_404(recipe_id)
    if current_recipe.user_id == g.user.id:
        flash('Sorry! You are not allowed to like your own recipes.', 'warning')
        return redirect('/')

    user_likes = g.user.likes

    if current_recipe in user_likes:
        g.user.likes = [like for like in user_likes if like != current_recipe]
    else:
        g.user.likes.append(current_recipe)
    # pdb.set_trace()

    try:
        db.session.commit()
    except Exception as e:
        print(e)

    return redirect('/users/search', code=307)
    


# ------- Recipes route ------- #

@app.route('/recipes/add', methods=['GET', 'POST'])
def add_recipe():
    '''Add a new recipe.'''

    if not g.user:
        flash('Access unauthorized', 'danger')
        return redirect('/')

    form = AddRecipeForm()
    # pdb.set_trace()
    if form.validate_on_submit():
        recipe = Recipe(
            title =form.title.data,
            recipe_image =form.recipe_image.data,
            dish_type =form.dish_type.data,
            cuisine_type =form.cuisine_type.data,
            recipe =form.recipe.data
        )
        
        g.user.recipes.append(recipe)
        db.session.commit()

        return redirect(f'/users/{g.user.id}/recipes')

    return render_template('recipes/new.html', form=form)


@app.route('/recipes/<int:recipe_id>/delete', methods=['POST'])
def delete_recipe(recipe_id):
    '''Delete recipes.'''

    if not g.user:
        flash('Access unauthorized', 'danger')
        return redirect('/')

    recipe = Recipe.query.get_or_404(recipe_id)
    db.session.delete(recipe)
    db.session.commit()

    return redirect(f'/users/{g.user.id}/recipes')


# ------- Home route ------- #

@app.route('/')
def homepage():
    '''Show homepage.'''

    recipes = Recipe.query.all()

    if g.user:
        liked_recipe_ids = [recipe.id for recipe in g.user.likes]
    
        return render_template('homepage.html', recipes=recipes, likes=liked_recipe_ids)
    
    return render_template('homepage-anon.html')

    