from cgitb import text
from datetime import datetime
from email.policy import default

#from email.policy import default
from sqlalchemy.types import Boolean,Date,DateTime,Float,Integer,Text,Time,Interval
from flaskapp import db,login_manager,app
from flaskapp.config import Config
from flask_login import UserMixin
from alembic import op
branche_labels = None
depends_on = None

from itsdangerous import URLSafeTimedSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(25),nullable=False)
    lname = db.Column(db.String(25),nullable=False)
    username = db.Column(db.String(25),unique=True,nullable=False)
    email= db.Column(db.String(125),unique = True ,nullable=False)
    image_file = db.Column(db.String(20),nullable=False,default='crypto.jpg')
    password = db.Column(db.String(60),nullable=False)
    bio = db.Column(db.Text,nullable=True)
    admin = db.Column(db.Boolean,nullable=True,default=False)
    lessons= db.relationship("Lesson", backref="author", lazy=True)
    def get_reset_token(self):
        s = Serializer(app.config['SECRET_KEY'],salt='pw-reset')
        return s.dumps({'user_id':self.id})
    @staticmethod
    def verify_reset_token(token,age=3600):
        s = Serializer(app.config['SECRET_KEY'],salt='pw-reset')
        try:
            user_id = s.loads(token,max_age=age)['user_id']
        except:
            return None
        return User.query.get(user_id)
    def __repr__(self):
        return f"User('{self.fname}','{self.lname}','{self.username}','{self.email}','{self.admin}','{self.image_file}')"


class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    date_posted = db.Column(db.DateTime,nullable=False,default=datetime.utcnow())
    description = db.Column(db.String(500),nullable=False)
    content = db.Column(db.Text,nullable=False)
    thumbnail = db.Column(db.String(25),nullable=False,default='crypto.jpg')
    slug = db.Column(db.String(32),unique = True,nullable=False)
    sources = db.Column(db.String(540),nullable=False,default='fff')
    #field = db.Column(db.String(25),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"),nullable=False)
    field_id = db.Column(db.Integer, db.ForeignKey("field.id"),nullable=False)

    def __repr__(self):
        return f"Lesson('{self.title}','{self.date_posted}')"



class Field(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150),nullable=False)
    descriptions = db.Column(db.String(500),nullable=False)
    icon = db.Column(db.String(25),nullable=False,default='crypto.jpg')
    lessons= db.relationship("Lesson", backref="field_name", lazy=True)
    def __repr__(self):
        return f"Field('{self.title}','{self.descriptions}'"

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(130),nullable=False)
    date_posted = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    description = db.Column(db.String(240),nullable=False)
    link_book = db.Column(db.String(130),nullable=False)
    icon_book = db.Column(db.String(25),nullable=False,default='crypto.jpg')
    slug = db.Column(db.String(32),nullable=False)

    def __repr__(self):
        return f"Book('{self.title}','{self.date_posted}')"


class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250),nullable=False)
    date_posted = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    content = db.Column(db.Text,nullable=False)
    thumbnail = db.Column(db.String(25),nullable=False,default='crypto.jpg')
    slug = db.Column(db.String(32),unique = True,nullable=False)
    sources = db.Column(db.String(255),nullable=False,default='fff')

    def __repr__(self):
        return f"Book('{self.title}','{self.date_posted}')"