from flask import render_template, request, Blueprint, url_for
from flask_login import current_user
from companyBlog.models import BlogPost

core = Blueprint('core',__name__)

@core.route('/')
def index():
    page = request.args.get('page',1,type=int)
    blog_posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page,per_page=5)
    if current_user.is_authenticated:
        profile_image = url_for('static', filename='profile_pics/' + current_user.profile_image)
    else:
        profile_image = url_for('static', filename='profile_pics/' + "default.png")
    return render_template('index.html.j2',blog_posts=blog_posts,profile_image=profile_image)


@core.route('/info')
def Info():
    return render_template('info.html.j2')
