from app import db
from flask import render_template, flash, url_for, redirect, request, abort, Blueprint
from app.posts.forms import PostForm
from app.models import User, Post
from flask_login import current_user, login_required

posts = Blueprint('posts', __name__)


@posts.route('/post/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=4)
    return render_template('user_posts.html', title=user.username +'Posts', posts=posts, user=user)


# =============================== Post Routes =============================================

@posts.route('/post/new', methods=['POST', 'GET'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, tags=form.tags.data, description=form.description.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post created', category='success')
        return redirect(url_for('main.index'))
    return render_template('new_post.html', title="Add new Post", form=form, legend='Create Post')


@posts.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route('/post/<int:post_id>/update', methods=['POST', 'GET'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data 
        post.tags=form.tags.data
        post.description=form.description.data
        post.content=form.content.data
        db.session.commit()
        flash('Post updated!', category='success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.tags.data = post.tags
        form.description.data = post.description
        form.content.data = post.content
    return render_template('new_post.html', title='Update ' + post.title, post=post, form=form, legend='Update Post')


@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted!', category='success')
    return redirect(url_for('main.index'))

