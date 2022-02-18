import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Recipe, Likes

os.environ['DATABASE_URL'] = 'postgresql:///capstone_one_test'

from app import app, CURR_USER_KEY

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False


# ------- Views ------- #

class UserViewTestCase(TestCase):
    '''Test views for users.'''

    def setUp(self):
        '''Create test client and add sample data.'''

        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.testuser1 = User.signup(
            username='testuser1',
            email='email1@email.com',
            password='testuser'
        )
        self.testuser1_id = 1111
        self.testuser1.id = self.testuser1_id

        db.session.commit()
    
    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp


    # ------- User View ------- #

    def test_show_unauthorized_recipes_page(self):
        '''Testing if the users are not logged in, were they disallowed to visting 'recipes' page.'''

        with self.client as c:
            
            response = c.get(f'/users/{self.testuser1_id}/recipes', follow_redirects=True)

            self.assertEqual(response.status_code, 200)
            self.assertNotIn('testuser1', str(response.data))
            self.assertIn('Access unauthorized', str(response.data))


    def test_show_unauthorized_likes_page(self):
        '''Testing if the users are not logged in, were they disallowed to visting 'likes' page.'''

        with self.client as c:
            
            response = c.get(f'/users/{self.testuser1_id}/likes', follow_redirects=True)

            self.assertEqual(response.status_code, 200)
            self.assertNotIn('testuser1', str(response.data))
            self.assertIn('Access unauthorized', str(response.data))


    # ------- Recipe View ------- #

    # def test_add_recipe(self):
    #     '''Test if user can add a recipe.'''

    #     with self.client as c:
    #         with c.session_transaction() as sess:
    #             sess[CURR_USER_KEY] = self.testuser1.id

    #         response = c.post('/recipes/add', 
    #             data={
    #                 'title': 'Test Recipe 1', 
    #                 'recipe_image': 'image1', 
    #                 'dish_type': 'dishtype1', 
    #                 'cuisine_type': 'cuisinetype1', 
    #                 'recipe': 'steps11111111111',
    #             })

    #         self.assertEqual(response.status_code, 200)

    #         recipe = Recipe.query.first()
    #         print(recipe)
    #         self.assertEqual(recipe.title, 'Test Recipe 1')


    def test_delete_recipe(self):
        'Test if user can delete a recipe.'

        recipe = Recipe(id=1111, title='Test Recipe 1', recipe_image='image1', dish_type='dishtype1', cuisine_type='cuisinetype1', recipe='steps1', user_id=self.testuser1_id)
        db.session.add(recipe)
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser1.id

            response = c.post('/recipes/1111/delete', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

            recipe = Recipe.query.get(1111)
            self.assertIsNone(recipe)

    def test_unauthenticated_recipe_add(self):
        '''Test if a user logged out, he can't add recipes anymore.'''

        with self.client as c:
            response = c.post('/recipes/add', follow_redirects=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('Access unauthorized', str(response.data))

    def test_unauthenticated_recipe_delete(self):
        '''Test if a user logged out, he can't delete recipes anymore.'''

        recipe = Recipe(id=1111, title='Test Recipe 1', recipe_image='image1', dish_type='dishtype1', cuisine_type='cuisinetype1', recipe='steps1', user_id=self.testuser1_id)
        db.session.add(recipe)
        db.session.commit()

        with self.client as c:
            response = c.post('/recipes/1111/delete', follow_redirects=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('Access unauthorized', str(response.data))

    def test_unauthorized_recipe_add(self):
        '''Test if a user logged in as another user, would he be able to add a recipe?'''

        recipe = Recipe(id=1111, title='Test Recipe 1', recipe_image='image1', dish_type='dishtype1', cuisine_type='cuisinetype1', recipe='steps1', user_id=self.testuser1_id)
        db.session.add(recipe)
        db.session.commit()

        unauthorized_user = User.signup(username='Unauthorized', email='email@email.com', password='password')
        unauthorized_user.id = 22222

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = 22222

            response = c.post('/recipes/add', follow_redirects=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('Access unauthorized', str(response.data))

    def test_unauthorized_recipe_delete(self):
        '''Test if a user logged in as another user, would he be able to delete a recipe?'''

        recipe = Recipe(id=1111, title='Test Recipe 1', recipe_image='image1', dish_type='dishtype1', cuisine_type='cuisinetype1', recipe='steps1', user_id=self.testuser1_id)
        db.session.add(recipe)
        db.session.commit()

        unauthorized_user = User.signup(username='Unauthorized', email='email@email.com', password='password')
        unauthorized_user.id = 22222

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = 22222

            response = c.post('/recipes/1111/delete', follow_redirects=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('Access unauthorized', str(response.data))


# -------  Models ------- #

class ModelsTestCase(TestCase):
    '''Test models for users.'''

    def setUp(self):
        '''Create test client and add sample data.'''

        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.testuser1 = User.signup(
            username='testuser1',
            email='email1@email.com',
            password='testuser'
        )
        self.testuser1_id = 1111
        self.testuser1.id = self.testuser1_id

        db.session.commit()
    
    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp


    # -------  User Model ------- #

    def test_user_model(self):
        '''Testing basic model.'''

        user = User(
            username='testuser',
            email='testuser@email.com',
            password='testuserpassword'
        )

        db.session.add(user)
        db.session.commit()

        self.assertEqual(len(user.recipes), 0)
        self.assertEqual(len(user.likes), 0)

    def test_valid_signup(self):
        '''Testing can users create accounts successfully with valid credentials.'''

        new_test_user = User.signup('newtestuser', 'newtestuser@email.com', 'newtestuserpassword')
        new_test_user_id = 2222
        new_test_user.id = new_test_user_id

        db.session.commit()

        new_test_user = User.query.get(new_test_user_id)

        self.assertEqual(new_test_user.username, 'newtestuser')
        self.assertEqual(new_test_user.email, 'newtestuser@email.com')
        self.assertNotEqual(new_test_user.password, 'newtestuserpassword')
        self.assertTrue(new_test_user.password.startswith('$2b$'))

    def test_invalid_signup(self):
        '''Testing unique usernames, not null email and password sign up.'''

        non_uniqueness_username = User.signup('testuser1', 'testuser@email.com', 'password')
        non_uniqueness_username_id = 11111
        non_uniqueness_username.id = non_uniqueness_username_id
        
        empty_username = User.signup('' or None, 'testuser@email.com', 'password')
        empty_username_id = 22222
        empty_username.id = empty_username_id

        empty_email = User.signup('testuser2', '' or None, 'password')
        empty_email_id = 22222
        empty_email.id = empty_email_id

        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

        with self.assertRaises(ValueError) as context:
            User.signup('testuser1', 'testuser@email.com', '' or None)

    def test_valid_authentication(self):
        '''Test if user can log in succssefully with correct credentials.'''

        user = User.authenticate(self.testuser1.username, 'testuser')

        self.assertIsNotNone(user)
        self.assertEqual(user.id, self.testuser1_id)

    def test_invalid_authentication(self):
        '''Test correct username and password.'''

        self.assertFalse(User.authenticate('wrongusername', 'testuser'))
        self.assertFalse(User.authenticate(self.testuser1.username, 'wrongpassword'))


    # -------  Recipe Model ------- #


    def test_recipe_model(self):
        '''Test basic model of recipe.'''

        recipe = Recipe(id=1111, title='Test Recipe 1', recipe_image='image1', dish_type='dishtype1', cuisine_type='cuisinetype1', recipe='steps1', user_id=self.testuser1_id)
        db.session.add(recipe)
        db.session.commit()

        self.assertEqual(len(self.testuser1.recipes), 1)
        self.assertEqual(self.testuser1.recipes[0].title, 'Test Recipe 1')

    def test_like_recipe(self):
        '''Test if like a recipe works.'''

        recipe = Recipe(id=1111, title='Test Recipe 1', recipe_image='image1', dish_type='dishtype1', cuisine_type='cuisinetype1', recipe='steps1', user_id=self.testuser1_id)
        db.session.add(recipe)
        db.session.commit()

        new_test_user = User.signup('newtestuser', 'newtestuser@email.com', 'newtestuserpassword')
        new_test_user_id = 2222
        new_test_user.id = new_test_user_id

        db.session.add_all([recipe, new_test_user])
        db.session.commit()

        new_test_user.likes.append(recipe)

        db.session.commit()

        like = Likes.query.filter(Likes.user_id == new_test_user_id).all()
        self.assertEqual(len(like), 1)

