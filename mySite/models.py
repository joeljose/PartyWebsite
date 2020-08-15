from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from mySite import db, login_manager
from flask_login import UserMixin



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    district = db.Column(db.String(20),nullable=False,default='default')
    localBodyType = db.Column(db.String(20),nullable=False,default='default')
    localBodyName = db.Column(db.String(20),nullable=False,default='default')
    phone = db.Column(db.String(20),nullable=False,default='default')
    privelege=db.Column(db.Integer,nullable=False,default=0)  
    verify_email=db.Column(db.Boolean,nullable=False,default=False) 
    verify_phone=db.Column(db.Boolean,nullable=False,default=False) 
    posts = db.relationship('Post', backref='author', lazy=True)


    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"




class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status=db.Column(db.Integer,nullable=False,default=0)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
    
    
    
    
    
class District_name(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    body_name = db.relationship('Body_name', backref='district', lazy=True)
    
    def __repr__(self):
        return f"District('{self.id}', '{self.name}')"
    
    
    
    
class Body_type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    body_name = db.relationship('Body_name', backref='body', lazy=True)
    
    def __repr__(self):
        return f"LocalBodyType('{self.id}', '{self.name}')"
    
    
    
    
class Body_name(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    district_id = db.Column(db.Integer, db.ForeignKey('district_name.id'), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('body_type.id'), nullable=False)
    
    def __repr__(self):
        return f"LocalBodyName('{self.name}', '{self.body.name}', '{self.district.name}')"
