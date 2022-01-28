from inspect import ismethoddescriptor
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    '''Users.'''

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)

    meals = db.relationship('Meal')
    dish_type = db.relationship('Dish')
    cuisine_type = db.relationship('Cuisine')

    @classmethod
    def signup(cls, username, email, password):
        '''Sign up user and hashes the password.'''

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(username=username, email=email, password=hashed_pwd)

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        '''Login user and to check if the username and the password matching with the ones in the database.'''

        user = cls.query.filter_by(username=username).first()

        if user:
            is_authenticated = bcrypt.check_password_hash(user.password, password)
            if is_authenticated:
                return user

        return False


class Dish(db.Model):
    '''Dish types.'''
    
    __tablename__ = 'dish_types'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)


class Cuisine(db.Model):
    '''Cuisine types.'''
    
    __tablename__ = 'cuisine_types'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)


class Recipe(db.Model):
    '''Recipes.'''
    
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    ingredients = db.relationship('Ingredient')


class Ingredient(db.Model):
    '''Ingredients.'''
    
    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)


class Meal(db.Model):
    '''Meals.'''

    __tablename__ = 'meals'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=True)
    meal_image = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))
    dish_type_id = db.Column(db.Integer, db.ForeignKey('dish_types.id', ondelete='cascade'))
    cuisine_type_id = db.Column(db.Integer, db.ForeignKey('cuisine_types.id', ondelete='cascade'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id', ondelete='cascade'))



def connect_db(app):
    db.app = app
    db.init_app(app)
