from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import hashlib
from app import login




class User(UserMixin,db.Model):

    def set_password(self, password):
            self.password = hashlib.sha256(password.encode('ascii')).hexdigest()

    def check_password(self, password):
            return self.password == hashlib.sha256(password.encode('ascii')).hexdigest()

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64),index=True,unique=True)
    FirstName = db.Column(db.String(64),index=True)
    LastName = db.Column(db.String(64),index=True)
    email = db.Column(db.String(64),index=True,unique=True)
    password = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
