from flask import request
import requests
from models import db, User, Recipe
from app import app

db.drop_all()
db.create_all()

response = requests.get('https://api.edamam.com/api/recipes/v2?type=public', 
        params={
            'q': 'chicken',
            'app_id': 'd097d304',
            'app_key': 'ccb5ad1a079a4045adc90a739f7f2785'
        }
    )

recipes = response.json()

sample_user = User.signup(username='Recipe King', email='recipeking@email.com', password='thekingishere')

db.session.add(sample_user)

for recipe in recipes['hits']:
    new_dict = {k: v for k, v in recipe['recipe'].items() if k in {'label', 'image',  'ingredientLines', 'cuisineType', 'dishType', 'url'}}
    new_recipe = Recipe(
        title=new_dict['label'], 
        recipe_image=new_dict['image'], 
        url=new_dict['url'], 
        recipe=new_dict['ingredientLines'], 
        cuisine_type=new_dict['cuisineType'][0].capitalize(), 
        dish_type=new_dict['dishType'][0].capitalize()
    )

    db.session.add(new_recipe)
    sample_user.recipes.append(new_recipe)
 


db.session.commit()

            
