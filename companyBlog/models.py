from companyBlog import db, login_manager, app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    profile_image = db.Column(db.String(64),nullable=False,default='default.png')
    email = db.Column(db.String(64),unique=True,index = True)
    username = db.Column(db.String(64),unique=True,index=True)
    password_hash = db.Column(db.String(128))

    posts = db.relationship('BlogPost',backref='author',lazy=True)
    comments = db.relationship('Comment', backref='commentUser',lazy=True)

    def get_reset_token(self,expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'],expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod # this tells python this is a static function and
                  # not to expect self object
    def validate_reset_token(token):
        s= Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
    def __init__(self,email,username,password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def validate_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f"Username {self.username}"

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.Text,nullable=False)
    date = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('blog_post.id'))
    users = db.relationship(User)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    def __repr__(self):
        return f"Post ID: {self.post_id} -- Comment ID: {self.id} -- Date: {self.date}"

class BlogPost(db.Model):
    users = db.relationship(User)

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)

    date = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    title = db.Column(db.String(140),nullable=False)
    # text = db.Column(db.Text,nullable=False)
    html = db.Column(db.Text)
    comments = db.relationship('Comment', lazy=True)

    def __init__(self,title,html,user_id,author):
        self.title = title
        self.html = html
        self.user_id = user_id
        self.author = author

    def __repr__(self):
        return f"Post ID: {self.id} -- Date {self.date} -- Html {self.html}"

