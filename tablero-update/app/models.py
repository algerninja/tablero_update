from flask import jsonify
from flask_login import UserMixin
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

from . import mongo
from . import login_manager
from . import mail


class User(UserMixin):
    
    def __init__(self, email = None, id = None, username = None, name=None, password=None):
        self._db = mongo.db.user
        self.password = password
        self.email = email
        self._id = self._db.find_one({'email': self.email},{'_id':1})
        
        if self._id:
            self._id = str(self._id['_id'])

    
    def get_id(self):
        return self._id


    def get_id_obj(self):
        return ObjectId(self._id)


    def get(self):
        user = self._db.find_one({'_id': self.get_id_obj()})
        if user:
            user['_id'] = str(user.get('_id'))
        
        return user

    @login_manager.user_loader
    def load_user(user_id):
        datos = mongo.db.user.find_one({'_id':ObjectId(user_id)},{'email':1})
        return User(email=datos.get('email'))

    @property
    def is_authenticated(self):
        return True

    
    @property
    def is_active(self):
        return True

    def check_password(self):
        user = self._db.find_one({'_id': self.get_id_obj()},{'password':1})

        password_hash = user.get('password') if user else '0'

        return check_password_hash(password_hash, self.password)