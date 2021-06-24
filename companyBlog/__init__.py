import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = "mysecret"

############################
######## Database Setup ####
############################

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://urbdgwiqvsxstj:4828407807408771919315eca5dff6877e6ae0896ca8ce69b13cd0d286b61d89@ec2-35-174-35-242.compute-1.amazonaws.com:5432/d5i81fdskjitbi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

############################
###### LOGIN MANAGER #######
############################
login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = 'users.login'

###################
###### MAIL #######
###################

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.getenv("EMAIL_USER")
app.config['MAIL_PASSWORD'] = os.getenv("EMAIL_PASS")

mail = Mail(app)

from companyBlog.core.views import core
from companyBlog.error_pages.handlers import error_pages
from companyBlog.users.views import users
from companyBlog.blog_posts.views import blog_posts


app.register_blueprint(blog_posts)
app.register_blueprint(users)
app.register_blueprint(core)
app.register_blueprint(error_pages)
