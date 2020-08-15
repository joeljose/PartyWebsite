from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from mySite.models import User, Post, Body_type, Body_name, District_name
import phonenumbers


class NonValidatingSelectField(SelectField):
    def pre_validate(self, form):
        pass

class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    district = NonValidatingSelectField('District', choices = [],coerce=int,validators=[DataRequired()])
    lsg_type = NonValidatingSelectField('LSG type', choices = [],coerce=int,validators=[DataRequired()])
    lsg_name = NonValidatingSelectField('LSG name', choices = [],validators=[DataRequired()],coerce=int)
    phone = StringField('Phone',validators=[DataRequired(),Length(min=10,max=16)])
    submit = SubmitField('Sign Up')
    
    def validate_district(self,district):
        if district.data==None:
            raise ValidationError('Please Select an option.')
            
    def validate_lsg_type(self,lsg_type):
        if lsg_type.data==None:
            raise ValidationError('Please Select an option.')
            
    def validate_lsg_name(self,lsg_name):
        if lsg_name.data==None:
            raise ValidationError('Please Select an option.')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')
            
#    def validate_phone(self, phone):
#        if len(phone.data) > 16:
#            raise ValidationError('Invalid phone number.')
#        try:
#            input_number = phonenumbers.parse(phone.data)
#            if not (phonenumbers.is_valid_number(input_number)):
#                raise ValidationError('Invalid phone number.')
#        except:
#            input_number = phonenumbers.parse("+91"+phone.data)
#            if not (phonenumbers.is_valid_number(input_number)):
#                raise ValidationError('Invalid phone number.')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')
    
    
    
    district = NonValidatingSelectField('District', choices = [],coerce=int,validators=[DataRequired()])
    lsg_type = NonValidatingSelectField('LSG type', choices = [],coerce=int,validators=[DataRequired()])
    lsg_name = NonValidatingSelectField('LSG name', choices = [],validators=[DataRequired()],coerce=int)
    phone = StringField('Phone',validators=[DataRequired(),Length(min=10,max=16)])
    
    def validate_district(self,district):
        if district.data==None:
            raise ValidationError('Please Select an option.')
            
    def validate_lsg_type(self,lsg_type):
        if lsg_type.data==None:
            raise ValidationError('Please Select an option.')
            
    def validate_lsg_name(self,lsg_name):
        if lsg_name.data==None:
            raise ValidationError('Please Select an option.')
    
    
    

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')
                



class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')



class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
