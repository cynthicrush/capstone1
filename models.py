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

    recipes = db.relationship('Recipe')
    likes = db.relationship('Recipe', secondary='likes')

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


class Recipe(db.Model):
    '''Recipes.'''

    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    recipe_image = db.Column(db.Text, nullable=False)
    dish_type = db.Column(db.Text, nullable=False)
    cuisine_type = db.Column(db.Text, nullable=False)
    recipe = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))


    user = db.relationship('User', overlaps='recipes')


class Likes(db.Model):
    '''Mapping user likes.'''

    __tablename__ = 'likes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id', ondelete='cascade'))


def connect_db(app):
    db.app = app
    db.init_app(app)
