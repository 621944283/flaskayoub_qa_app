from flask import Blueprint
from flask_admin.contrib.sqla import ModelView
from flask import redirect,url_for
from flask_admin import AdminIndexView

from flask_login import LoginManager,current_user

from flaskapp import admin,db
from flaskapp.models import User,Lesson,Field,Book,Education

adminpn = Blueprint('adminpn',__name__)

class Controller(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated
    def not_auth(self, name , **kwargs):
        return "sorry you need permission to access in page admin"

class myadminindexview(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.id==1:
            return current_user.is_authenticated
    def not_auth(self, name , **kwargs):
        return redirect(url_for('users.login'))
from flaskapp.models import User
admin.add_view(Controller(User,db.session))
admin.add_view(Controller(Lesson,db.session))
admin.add_view(Controller(Field,db.session))
admin.add_view(Controller(Book,db.session))
admin.add_view(Controller(Education,db.session))




