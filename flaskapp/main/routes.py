
from flask import render_template,url_for,flash,redirect,request
from flaskapp import app
from flask_login import login_user,current_user,logout_user,login_required
from flask import Blueprint
from flaskapp.models import Education, User,Lesson,Book,Field

main = Blueprint('main',__name__)


@main.route('/')

def home():
    page = request.args.get('page',1,type=int)
    lessons = Lesson.query.order_by(Lesson.date_posted.desc()).paginate(page=page,per_page=6)
    #lessons = Lesson.query.paginate(page=page,per_page=6)
    user = User.query.all()
    fields = Field.query.all()
    
    return render_template('home.html',active_tab='home',user=user,lessons=lessons,fields=fields)


@main.route('/about')
def about():
    
    lessons = Lesson.query.all()
    user = User.query.all()
    fields = Field.query.all()
    return render_template('about.html',active_tab='about',lessons=lessons,user=user,fields=fields)


@main.route('/education',methods=['POST','GET'])
def education():
    
    lessons = Lesson.query.all()
    user = User.query.all()
    fields = Field.query.all()
    education = Education.query.all() 
    return render_template('education.html',active_tab='education',lessons=lessons,user=user,fields=fields,education=education)

@main.route('/bibliotheque')
def bibliotheque():
    
    lessons = Lesson.query.all()
    user = User.query.all()
    book = Book.query.all()
    fields = Field.query.all()
    return render_template('bibliotheque.html',active_tab='bibliotheque',lessons=lessons,user=user,book=book,fields=fields)


@main.route('/all field')
def field():
    
    lessons = Lesson.query.all()
    user = User.query.all()
    book = Book.query.all()
    fields = Field.query.all()
    return render_template('field.html',active_tab='all field',lessons=lessons,fields=fields,user=user,book=book)

