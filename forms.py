from flask_wtf import FlaskForm
import validators
from wtforms import StringField, PasswordField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

dish_types = [('Alcohol-cocktail', 'Alcohol-cocktail'), ('Biscuits and cookies', 'Biscuits and cookies'), ('Bread', 'Bread'), ('Cereals', 'Cereals'), ('Condiments and sauces', 'Condiments and sauces'), ('Drinks', 'Drinks'), ('Desserts', 'Desserts'), ('Egg', 'Egg'), ('Main course', 'Main course'), ('Omelet', 'Omelet'), ('Pancake', 'Pancake'), ('Preps', 'Preps'), ('Preserve', 'Preserve'), ('Salad', 'Salad'), ('Sandwiches', 'Sandwiches'), ('Soup', 'Soup'), ('Starter', 'Starter')]

cuisine_types = [('American', 'American'), ('Asian', 'Asian'), ('British', 'British'), ('Caribbean', 'Caribbean'), ('Central Europe', 'Central Europe'), ('Chinese', 'Chinese'), ('Eastern Europe', 'Eastern Europe'), ('French', 'French'), ('Indian', 'Indian'), ('Italian', 'Italian'), ('Japanese', 'Japanese'), ('Kosher', 'Kosher'), ('Mediterranean', 'Mediterranean'), ('Mexican', 'Mexican'), ('Middle Eastern', 'Middle Eastern'), ('Nordic', 'Nordic'), ('South American', 'South American'), ('South East Asian', 'South East Asian')]


class SignupForm(FlaskForm):
    '''Signup form.'''

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=8)])


class LoginForm(FlaskForm):
    '''Login form.'''

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=8)])


class AddRecipeForm(FlaskForm):
    '''Add a new recipe form.'''

    title = StringField('Title', validators=[DataRequired()])
    recipe_image = StringField('Recipe Image', validators=[DataRequired()])
    dish_type = SelectField('Dish Type', choices=dish_types)
    cuisine_type = SelectField('Cuisine Type', choices=cuisine_types)
    recipe = TextAreaField('Recipe', validators=[Length(min=10)])



