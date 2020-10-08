from flask import render_template, request, Blueprint
from mySite.models import Post

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(status=1).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)
#    return render_template('under.html')


@main.route("/approve")
def approve_post():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(status=0).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('approve.html', posts=posts)



@main.route("/about")
def about():
    return render_template('about.html', title='About')
#    return render_template('under.html')