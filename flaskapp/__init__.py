
from flask import Flask,redirect,url_for
from flask_admin import Admin,AdminIndexView

from flask_sqlalchemy import SQLAlchemy
import pymysql
from flaskapp.config import Config
from flask_bcrypt import Bcrypt
from flask_login import LoginManager,login_user,current_user,logout_user
from flask_migrate import Migrate
from flask_ckeditor import CKEditor
from flask_modals import Modal
from flask_mail import Mail


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
ckeditor = CKEditor()
modal = Modal()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()

admin = Admin(name='AyoubTechno',template_mode='bootstrap3')




def create_app(config_app=Config):
    migrate.init_app(app,db,render_as_batch=True)
    from flaskapp.adminpn.routes import myadminindexview
    db.init_app(app)
    bcrypt.init_app(app)
    #migrate.init_app(app,db)
    login_manager.init_app(app)
    ckeditor.init_app(app)
    modal.init_app(app)
    admin.init_app(app,index_view=myadminindexview())
    mail.init_app(app)
    with app.app_context():
        from flaskapp.models import User,Book,Lesson,Field
        #db.drop_all()
        db.create_all()

    from flaskapp.main.routes import main
    from flaskapp.users.routes import users
    from flaskapp.adminpn.routes import adminpn
    
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(adminpn)
    return app