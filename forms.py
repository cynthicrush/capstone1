from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

dish_types = [('alcohol-cocktail', 'Alcohol-cocktail'), ('biscuits-cookies', 'Biscuits and cookies'), ('bread', 'Bread'), ('cereals', 'Cereals'), ('condiments-sauces', 'Condiments and sauces'), ('drinks', 'Drinks'), ('desserts', 'Desserts'), ('egg', 'Egg'), ('main-course', 'Main course'), ('omelet', 'Omelet'), ('pancake', 'Pancake'), ('preps', 'Preps'), ('preserve', 'Preserve'), ('salad', 'Salad'), ('sandwiches', 'Sandwiches'), ('soup', 'Soup'), ('starter', 'Starter')]

cuisine_types = [('american', 'American'), ('asian', 'Asian'), ('british', 'British'), ('caribbean', 'Caribbean'), ('central-europe', 'Central Europe'), ('chinese', 'Chinese'), ('eastern-europe', 'Eastern Europe'), ('french', 'French'), ('indian', 'Indian'), ('italian', 'Italian'), ('japanese', 'Japanese'), ('kosher', 'Kosher'), ('mediterranean', 'Mediterranean'), ('mexican', 'Mexican'), ('middle-eastern', 'Middle Eastern'), ('nordic', 'Nordic'), ('south-american', 'South American'), ('south-east-asian', 'South East Asian')]


class SignupForm(FlaskForm):
    '''Signup form.'''

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=8)])


class LoginForm(FlaskForm):
    '''Login form.'''

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=8)])


class AddMealForm(FlaskForm):
    '''Add a new meal form.'''

    title = StringField('Title', validators=[DataRequired()])
    meal_image = StringField('Meal Image', validators=[DataRequired()])
    dish_type = SelectField('Dish Type', choices=dish_types)
    cuisine_type = SelectField('Cuisine Type', choices=cuisine_types)
    recipe = TextAreaField('Recipe', validators=[Length(min=10)])



