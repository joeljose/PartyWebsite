from flask import render_template, request, Blueprint, redirect
from mySite.models import Post

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/index")
def index():
    return render_template('index.html',title='Intro')


@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(status=1).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, title="Blog")
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

@main.route("/manifesto")
def manifesto():
    # with open('static/manifesto.pdf', 'rb') as static_file:
    #     return send_file(static_file, attachment_filename='manifesto.pdf')
    return redirect("static/manifesto.pdf")