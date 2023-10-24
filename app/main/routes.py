from flask import render_template, request, Blueprint
from app.models import Post


main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
@main.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=4)
    return render_template('index.html', title='Home Page', posts=posts)


@main.route('/about')
def about_page():
    return render_template('about.html', title="About Page")

