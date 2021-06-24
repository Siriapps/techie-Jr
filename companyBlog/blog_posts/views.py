from flask import render_template,url_for,flash,request,redirect,Blueprint
from flask_login import current_user,login_required
from werkzeug.exceptions import abort


from companyBlog import db
from companyBlog.models import BlogPost, Comment
from companyBlog.blog_posts.forms import BlogPostForm, CommentForm

blog_posts = Blueprint('blog_posts',__name__)

# CREATING
@blog_posts.route('/create',methods=['GET','POST'])
@login_required
def create_post():
    form = BlogPostForm()
    if request.method == 'POST':
        blog_post = BlogPost(title = form.title.data,
                             html=request.form.get('editordata'),
                             user_id=current_user.id,
                             author = current_user)
        db.session.add(blog_post)
        db.session.commit()
        flash("Blog Post Created",'success')
        return redirect(url_for('core.index'))

    return render_template('create_post.html.j2',form=form, title="Create a new blog post")


# BLOG POST (VIEW)
@blog_posts.route('/<int:blog_post_id>',methods=['GET','POST'])
def blog_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    form = CommentForm()

    if form.validate_on_submit():
        if current_user.is_authenticated:
            writtenBy = current_user
        else:
            writtenBy = None
        comment = Comment(body = form.comment.data,
                          post_id= blog_post.id,
                          commentUser=writtenBy)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('blog_posts.blog_post', blog_post_id=blog_post.id))
    comments = Comment.query.filter_by(post_id=blog_post.id).order_by(Comment.date.desc())
    # profile_image = url_for('static', filename='profile_pics/' + current_user.profile_image)
    return render_template('blog_post.html.j2', b_id=blog_post.id, author=blog_post.author.username,prev_ans="",
                            date=blog_post.date,post=blog_post.html,title=blog_post.title,form=form,
                            comment=comments)

# UPDATE
@blog_posts.route('/<int:blog_post_id>/update',methods=['GET','POST'])
@login_required
def update(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)

    if blog_post.author != current_user:
        abort(403)

    form = BlogPostForm()

    if request.method == 'POST':
        blog_post.title = form.title.data
        blog_post.html = request.form.get('editordata')
        db.session.commit()
        flash("Blog Post Updated", "success")
        return redirect(url_for('blog_posts.blog_post', blog_post_id=blog_post.id))
    elif request.method == 'GET':
        form.title.data = blog_post.title
        blog_post.html = blog_post.html

    return render_template('create_post.html.j2',title='Update blog post',form=form, prev_ans=blog_post.html)

# DELETE
@blog_posts.route('/<int:blog_post_id>/delete',methods=['GET','POST'])
@login_required
def delete_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user and current_user.username != 'admin':
        abort(403)

    db.session.delete(blog_post)
    db.session.commit()
    flash("Blog Post is deleted","warning")
    return redirect(url_for('core.index'))
