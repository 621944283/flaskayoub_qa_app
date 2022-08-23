from cgi import print_arguments
from crypt import methods

import email

import os

import secrets

#from fileinput import filename
from flask import render_template,url_for,flash,redirect,request,session,send_from_directory,abort
from flaskapp import app,bcrypt,db
from flask import Blueprint
from flask_modals import render_template_modal
from flaskapp.main.routes import education
from flaskapp.users.forms import (BooksAdmin,NewLessonForm, adminLogin,adminRegister,
UpdateProfileForm,NewfieldForm,LessonUpdateForm,
EducationForm,ResetPasswordForm,RequestResetForm)
#from ..main.routes import field
from flask_login import login_user,current_user,logout_user,login_required
from flask_ckeditor import upload_success,upload_fail
from flaskapp.models import Education, User,Book,Lesson,Field
from .utels import save_picture
users = Blueprint('users',__name__)
from flaskapp.users import utels
from flaskapp import bcrypt,db,app,mail
from flask_mail import Message

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Robot.com app Password Reset Requset', sender="technoayoub777@gmail.com",
    recipients = [user.email],
    body = f''' To reset your Password visit the following Link:{url_for('users.reset_password' , token=token ,_external=True)} If you did not make this request please ignore this email''')

    mail.send(msg)



def delete_picture(picture_name,path):
    picture_path = os.path.join(app.root_path,path,picture_name)
    try:
        os.remove(picture_path)
    except:
        pass
@app.route('/files/<path:filename>')
def uploaded_files(filename):
    path = os.path.join(app.root_path, 'static/media')
    return send_from_directory(path, filename)

@app.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('upload')
    # Add more validations here
    extension = f.filename.split('.')[-1].lower()
    if extension not in ['jpg', 'gif', 'png', 'jpeg']:
        return upload_fail(message='File extention not allowed!')
    random_hex = secrets.token_hex(8)    
    image_name = random_hex+extension
    f.save(os.path.join(app.root_path, 'static/media', image_name))
    url = url_for('uploaded_files', filename=image_name)
    return upload_success(url, filename=image_name)  # return upload_success call




def get_previous_next_lesson(lesson):
    field = lesson.field_name
    for lsn in field.lessons:
        if lsn.title == lesson.title:
            index =  field.lessons.index(lsn)
            previous_lesson = field.lessons[index-1] if index > 0 else None
            next_lesson = field.lessons[index+1] if index < len(field.lessons)-1 else None
            break
    return previous_lesson,next_lesson

@users.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = adminRegister()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(fname=form.fname.data,lname=form.lname.data,username=form.username.data,
        email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Account Creat Successfully",'success')
        return redirect(url_for('users.login'))
    return render_template('adminregister.html',form=form)


@users.route('/login',methods=['GET','POST'])
def login():
    fields = Field.query.all()
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = adminLogin()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember=form.remember.data)
            flash("You have been Loged in ",'success')
            return redirect(url_for('users.dashboard'))
        else :
            flash("Login Unsuccessful please check credentials","danger")
        
    return render_template('adminlogin.html',form=form,fields=fields)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route('/dashboard',methods=['POST','GET'])
@login_required
def dashboard():
    lessons = Lesson.query.all()
    #user = User.query.all()
    book = Book.query.all()
    fields = Field.query.all()
    if current_user.admin == False:
        return abort(403)
    return render_template('dashboard.html',lessons=lessons,book=book,fields=fields)
 


@users.route('/dashboard/new_book',methods=['POST','GET'])
@login_required
def new_book():
    lessons = Lesson.query.all()
    #user = User.query.all()
    book = Book.query.all()
    fields = Field.query.all()
    form = BooksAdmin()
    active_tab = 'new_book'
    if form.validate_on_submit():
        if form.icon_book.data:
            picture_file = save_picture(form.icon_book.data,"static/icon_book",output_size=(300,300))
            
        book = Book(title=form.title.data,slug=form.slug.data,description=form.description.data,
        link_book=form.link_book.data,icon_book=picture_file)
        db.session.add(book)
        db.session.commit()
        flash('Books Has been Added in Bibliotheque','success')
        return redirect(url_for('users.dashboard'))
    return render_template('new_book.html',form=form,active_tab=active_tab,
    book=book,fields=fields,lessons=lessons)

@users.route("/dashboard/new_lesson",methods=['POST','GET'])
@login_required
def new_lesson():
    lessons = Lesson.query.all()
    #user = User.query.all()
    book = Book.query.all()
    fields = Field.query.all()
    new_lesson_form = NewLessonForm()
    new_field_form = NewfieldForm()
    form=""
    flag = session.pop("flag", False)
    if 'content' in request.form:
        form = 'new_lesson_form'
    elif 'descriptions' in request.form:
        form = 'new_field_form'
    
    if form =='new_lesson_form' and new_lesson_form.validate_on_submit():
        if new_lesson_form.thumbnail.data: 
                          
            picture_file = save_picture(new_lesson_form.thumbnail.data,"static/lesson_thumbnail",output_size=(300,300))
            
        lesson_slug = str(new_lesson_form.slug.data.replace(" ", "-")) 
        field = new_lesson_form.field.data
        lesson = Lesson(title=new_lesson_form.title.data,
        content=new_lesson_form.content.data,slug = lesson_slug,author = current_user,
        description=new_lesson_form.description.data,field_name = field,sources=new_lesson_form.sources.data,
        thumbnail=picture_file)
        db.session.add(lesson)
        db.session.commit()
        flash("new lesson has added",'success')
        return redirect(url_for("users.new_lesson"))
    elif form == 'new_field_form' and new_field_form.validate_on_submit():
        if new_field_form.icon.data:
            picture_file = save_picture(new_field_form.icon.data,"static/field_icon",output_size=(300,300))
        field_title = str(new_field_form.title.data).replace(" ","-")
        field = Field(title=field_title,descriptions=new_field_form.descriptions.data,icon=picture_file)
        db.session.add(field)
        db.session.commit()
        session['flag']=True
        flash("new field has been added",'success')
        return redirect(url_for("users.dashboard"))
           
           
       
           
    modal = None if flag else 'newField'
       
        
    return render_template_modal("new_lesson.html",new_lesson_form=new_lesson_form ,
    new_field_form=new_field_form,active_tab="new_lesson",modal=modal,
    lessons=lessons,fields=fields,book=book)
       
       
       

@users.route("/dashboard/profile",methods=['POST','GET'])
@login_required
def profile():
    lessons = Lesson.query.all()
    #user = User.query.all()
    book = Book.query.all()
    fields = Field.query.all()
    profile_form = UpdateProfileForm()
    if profile_form.validate_on_submit():
        if profile_form.picture.data:
            picture_file = save_picture(profile_form.picture.data,"static/user_pics")
            
            current_user.image_file = picture_file
        current_user.username = profile_form.username.data
        current_user.email = profile_form.email.data
        current_user.bio = profile_form.bio.data
        db.session.commit()
        flash("Your profile has been updated ",'success')
        return redirect(url_for("users.profile"))
    elif request.method == "GET":

        profile_form.username.data=current_user.username
        profile_form.email.data=current_user.email
        profile_form.bio.data=current_user.bio
    image_file = url_for("static", filename =f'user_pics/{current_user.image_file}')
    return render_template("profile.html", title="Profile",profile_form=profile_form ,
    image_file=image_file,active_tab="profile",
    lessons=lessons,book=book,fields=fields) 



@users.route("/<field>/<lesson_slug>")
def lesson(lesson_slug,field):
    fields =  Field.query.all()
    lesson=Lesson.query.filter_by(slug=lesson_slug).first()
    if lesson:
        previous_lesson,next_lesson = get_previous_next_lesson(lesson)
    lesson_id = lesson.id if lesson else None
    lesson=Lesson.query.get_or_404(lesson_id)
    return render_template('lesson_view.html',title=lesson.title,lesson=lesson,
    previous_lesson=previous_lesson,next_lesson=next_lesson,fields=fields)
  

@users.route("/<field_title>")
def field(field_title):
    #field_name = Field.query.filter_by(title=field.title).first()
    fields = Field.query.all()
    field = Field.query.filter_by(title=field_title).first()
    field_id = field.id if field else None
    field = Field.query.get_or_404(field_id)
    page = request.args.get('page',1,type=int)
    lessons = Lesson.query.filter_by(field_id=field_id).order_by(Lesson.date_posted.desc()).paginate(page=page,per_page=6)
    return render_template('field.html',title=field.title,field=field,fields=fields,active_tab='field',lessons=lessons)
  
@users.route('/dashboard/update_delete',methods=['GET','POST'])
@login_required
def update_delete():
    return render_template('update_delete.html',active_tab='update_delete')


@users.route("/<field>/<lesson_slug>/update",methods=['GET','POST'])
def update_lesson(lesson_slug,field):
    fields =  Field.query.all()
 
    
    lesson=Lesson.query.filter_by(slug=lesson_slug).first()
    if lesson:
        previous_lesson,next_lesson = get_previous_next_lesson(lesson)
    lesson_id = lesson.id if lesson else None
    lesson=Lesson.query.get_or_404(lesson_id)
    if lesson.author != current_user:
        abort(403)
    form = LessonUpdateForm()
    if form.validate_on_submit():
        lesson.field_name = form.field.data
        lesson.title = form.title.data
        lesson.description = form.description.data
        lesson.sources = form.sources.data
        lesson.slug = str(form.slug.data).replace(" ","-")
        lesson.content = form.content.data
        if form.thumbnail.data:
            delete_picture(lesson.thumbnail,"static/lesson_thumbnail")
            new_picture = save_picture(form.thumbnail.data,"static/lesson_thumbnail")
            lesson.thumbnail = new_picture
        db.session.commit()
        flash('your lesson has been update ','success')
        return redirect(url_for('users.lesson',lesson_slug=lesson.slug,field=lesson.field_name.title))
    elif request.method == "GET":
        print("HII")
        form.field.data = lesson.field_name.title
        form.title.data = lesson.title
        form.slug.data = lesson.slug
        form.description.data = lesson.description
        form.sources.data = lesson.sources
        form.content.data = lesson.content
    return render_template('update_lesson.html',title='Update | '+lesson.title,lesson=lesson,
    previous_lesson=previous_lesson,next_lesson=next_lesson,fields=fields,form=form)
  
@users.route("/lesson/<lesson_id>/delete",methods=['POST'])
def delete_lesson(lesson_id):
    #lesson_id=Lesson.query.filter_by(id=lesson.id).first()
    lesson = Lesson.query.get_or_404(lesson_id)
    if lesson.author != current_user:
        abort(403)
    db.session.delete(lesson)
    db.session.commit()
    flash('this lesson has been deleted','success')
    return redirect(url_for('users.update_delete'))


@users.route('/dashboard/add_education',methods=['POST','GET'])
@login_required
def add_education():
    lessons = Lesson.query.all()
    user = User.query.all()
    fields = Field.query.all()
    education = Education.query.all()
    education_form = EducationForm()
    if current_user.admin == True and current_user.id==1:
        if education_form.validate_on_submit():
            if education_form.thumbnail.data:
                picture_file = save_picture(education_form.thumbnail.data,"static/education_thumbnail",output_size=(300,300))
         
            education = Education(title = education_form.title.data,slug=education_form.slug.data,content=education_form.content.data,sources=education_form.sources.data,thumbnail=picture_file)
            db.session.add(education)
            db.session.commit()
            flash("Education has added",'success')
            return redirect(url_for("users.dashboard"))
        
    else:
        abort(403)
    
    return render_template('add_education.html',active_tab='add_education',education=education,education_form=education_form,lessons=lessons,user=user,fields=fields)





@users.route("/reset_password",methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
        flash('if this account exist, you will recive an email with instruction','info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html',title = 'Reset Password',form=form)


@users.route('/reset_password/<token>',methods=['GET','POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if not user:
        flash('the token is invalideor expired','warning')
        return redirect(url_for('users.reset_request')) 
    form =  ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password 
        db.session.commit()
        flash(f"Your Password has been  updated , You cannow log in",'success')
        return redirect(url_for('users.login'))
        
    return render_template('reset_password.html', title="Reset Password",form=form)

