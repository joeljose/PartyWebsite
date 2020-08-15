from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from mySite import db, bcrypt
from mySite.models import User, Post, Body_type, Body_name, District_name
from mySite.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from mySite.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    form.district.choices=[(district.id,district.name) for district in District_name.query.all()]
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        
        t_name=Body_type.query.filter_by(id=form.lsg_type.data).first().name
        d_name=District_name.query.filter_by(id=form.district.data).first().name
        l_name=Body_name.query.filter_by(id=form.lsg_name.data).first().name

        user = User(username=form.username.data, email=form.email.data,
                    password=hashed_password,localBodyType=t_name,
                    district=d_name,localBodyName=l_name,
                    phone=form.phone.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/register/districtSelect")
def returningDistrict():
    typeList=Body_type.query.all()
    typeArray=[]
    for a in typeList:
        typeObj={}
        typeObj['name']=a.name
        typeObj['id']=a.id
        typeArray.append(typeObj)
    return jsonify({'listOfTypes':typeArray})

@users.route("/register/nameSelect/<getString>")
def returningType(getString):
    getDistrict,getType=getString.split()
    t_id=int(getType)
    d_id=int(getDistrict)
    nameList = Body_name.query.filter_by(type_id=t_id,district_id=d_id).all()
    nameArray = []
    for lsgName in nameList:
        nameObj = {}
        nameObj['name'] = lsgName.name
        nameObj['id']= lsgName.id
        nameArray.append(nameObj)
    return jsonify({'lsgnames' : nameArray})



@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        
        
        current_user.localBodyType = Body_type.query.filter_by(id=form.lsg_type.data).first().name
        current_user.district = District_name.query.filter_by(id=form.district.data).first().name
        current_user.localBodyName = Body_name.query.filter_by(id=form.lsg_name.data).first().name
        
        current_user.phone = form.phone.data
        
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.phone.data = current_user.phone
        form.district.choices=[(District_name.query.filter_by(name=current_user.district).first().id,current_user.district)]
        form.lsg_name.choices=[(Body_name.query.filter_by(name=current_user.localBodyName).first().id,current_user.localBodyName)]
        form.lsg_type.choices=[(Body_type.query.filter_by(name=current_user.localBodyType).first().id,current_user.localBodyType)]
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@users.route("/register/districtClick")
def returningClick():
    districtList=District_name.query.all()
    distArray=[]
    for a in districtList:
        distObj={}
        distObj['name']=a.name
        distObj['id']=a.id
        distArray.append(distObj)
    return jsonify({'listOfdist':distArray})



@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
