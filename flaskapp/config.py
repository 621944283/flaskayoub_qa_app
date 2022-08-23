import os
import pymysql
class Config:
    SECRET_KEY= 'd71e327c04c11549fc8889cc652e781b54669d00927627ed5ddbb8a1baf44a2c'
    CKEDITOR_ENABLE_CODESNIPPET = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://youssef:pythonicyoussef@localhost/ayoub_db'
    #"sqlite:///ayoub.db"

    SQLALCHEMY_POOL_RECYCLE = 280
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_ADMIN_SWATCH = 'cerulean'
    CKEDITOR_ENABLE_CODESNIPPET = True
    CKEDITOR_FILE_UPLOADER = 'upload'

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    MAIL_USE_SSL = False