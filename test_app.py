import os
from unittest import TestCase

from models import db, User

# os.environ['DATABASE_URL'] = 'postgresql:///capstone_one_test'

from app import app, CURR_USER_KEY

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False


# ------- User view ------- #

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

