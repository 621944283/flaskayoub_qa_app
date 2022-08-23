from secrets import choice
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextAreaField
from wtforms.validators import DataRequired,Length,Email,Regexp,EqualTo,ValidationError
from flask_wtf.file import FileAllowed,FileField
from wtforms_sqlalchemy.fields import QuerySelectField
from flaskapp.models import User,Book,Lesson,Field
from flask_login import current_user
from flaskapp import ckeditor
from flask_ckeditor import CKEditorField
class adminRegister(FlaskForm):
    fname = StringField('First name',validators=[DataRequired(),Length(min=2,max=25)])
    lname = StringField('last name',validators=[DataRequired(),Length(min=2 ,max=25)])
    username = StringField('username',validators=[DataRequired(),Length(min=2 ,max=25)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired(),Regexp("^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,32}$")])
    confirm_password = PasswordField('confirm password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username Already Exist please choose a different username')

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email Already Exist please choose a different Email')
    
class adminLogin(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('submit')

class BooksAdmin(FlaskForm):
    title = StringField('Title book',validators=[DataRequired(),Length(min=2,max=25)])
    description = TextAreaField('Description Book',validators=[DataRequired(),Length(min=2 ,max=180)],render_kw={"rows" : "5"})
    link_book = StringField('Link Book',validators=[DataRequired(),Length(min=2 ,max=130)])
    slug = StringField('Slug',validators=[DataRequired(),Length(min=2 ,max=40)],render_kw={"placeholder" : "Descriptive short version of your title. Seo friendly"})
    icon_book = FileField("icon Book",validators=[DataRequired(),FileAllowed(["jpg","png"])])
    submit = SubmitField('Add Book')

def choice():
    return Field.query
class NewLessonForm(FlaskForm):
    field = QuerySelectField('Field',query_factory=choice,get_label="title")
    title = StringField('Title Lesson',validators=[DataRequired(),Length(min=2,max=25)])
    description = TextAreaField('Description Lesson',validators=[DataRequired(),Length(min=2,max=419)])
    thumbnail = FileField("Thumbnail",validators=[DataRequired(),FileAllowed(["jpg","png"])])
    #sources = StringField('Link sources',validators=[DataRequired(),Length(min=2 ,max=240)])
    sources = StringField('Source',validators=[DataRequired(),Length(min=2 ,max=540)],render_kw={"placeholder" : "Source link"})
    content = CKEditorField('Content Lesson',validators=[DataRequired()],render_kw={"rows" : "20"})
    slug = StringField('Slug',validators=[DataRequired(),Length(min=2 ,max=40)],render_kw={"placeholder" : "Descriptive short version of your title. Seo friendly"})
    submit = SubmitField('Add Lesson')
    def validate_slug(self,slug):
        lesson = Lesson.query.filter_by(slug=slug.data).first()
        if lesson :
            raise ValidationError('slug Already exit please chose defferente slug')
class UpdateProfileForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=2 ,max=25)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    bio = TextAreaField('Bio')
    picture = FileField('Update Profile',validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')
    def validate_username(self,username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user :
                raise ValidationError('username Already exit please chose defferente username')
    def validate_email(self,email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user :
                raise ValidationError('email Already exit please chose defferente email')



class NewfieldForm(FlaskForm):
    title = StringField('Title Field',validators=[DataRequired(),Length(min=2,max=35)])
    descriptions = TextAreaField('Description Field',validators=[DataRequired(),Length(max=419)],render_kw={"rows" : "4"})
    icon = FileField('icon Field',validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Add Field')
    def validate_title(self,title):
        field = Field.query.filter_by(title=title.data).first()
        if field :
            raise ValidationError(
                "Field name already exists Please choose different one"
            )


class LessonUpdateForm(NewLessonForm):
    thumbnail = FileField("Thumbnail",validators=[FileAllowed(["jpg","png"])])
    submit = SubmitField("Update")


class EducationForm(FlaskForm):
    title = StringField('Title Lesson',validators=[DataRequired(),Length(min=2,max=150)])
    thumbnail = FileField("Thumbnail",validators=[DataRequired(),FileAllowed(["jpg","png"])])
    #sources = StringField('Link sources',validators=[DataRequired(),Length(min=2 ,max=240)])
    sources = StringField('Source',validators=[DataRequired(),Length(min=2 ,max=540)],render_kw={"placeholder" : "Source link"})
    content = CKEditorField('Content Lesson',validators=[DataRequired()],render_kw={"rows" : "20"})
    slug = StringField('Slug',validators=[DataRequired(),Length(min=2 ,max=40)],render_kw={"placeholder" : "Descriptive short version of your title. Seo friendly"})
    submit = SubmitField('Add in Page Educatin')

class UpdateEducation(FlaskForm):
    title = StringField('Title Lesson',validators=[DataRequired(),Length(min=2,max=150)])
    thumbnail = FileField("Thumbnail",validators=[DataRequired(),FileAllowed(["jpg","png"])])
    #sources = StringField('Link sources',validators=[DataRequired(),Length(min=2 ,max=240)])
    sources = StringField('Source',validators=[DataRequired(),Length(min=2 ,max=540)],render_kw={"placeholder" : "Source link"})
    content = CKEditorField('Content Lesson',validators=[DataRequired()],render_kw={"rows" : "20"})
    slug = StringField('Slug',validators=[DataRequired(),Length(min=2 ,max=250)],render_kw={"placeholder" : "Descriptive short version of your title. Seo friendly"})
    submit = SubmitField('Add in Page Educatin')


class RequestResetForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    submit = SubmitField('Request Password Reset ')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password',validators=[DataRequired(),Regexp("^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,32}$")])
    confirm_password = PasswordField('confirm password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Reset  Password')
