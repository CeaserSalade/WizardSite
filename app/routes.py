from flask import Blueprint, render_template, redirect, url_for, request
from .models import User, db

main = Blueprint('main', __name__)

# Registration Route
@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return redirect(url_for('main.register'))  # Redirect back to register

        # Create new user
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('main.login'))  # Redirect to login after successful registration

    return render_template('register.html')


# Login Route
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if user exists
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            return redirect(url_for('main.home'))  # Redirect to home after successful login
        else:
            return redirect(url_for('main.login'))  # Redirect back to login on failure

    return render_template('login.html')


# Dashboard Route (After login)
@main.route('/home')
def home():
    return render_template('home.html')

@main.route('/')
def index():
    return render_template('index.html')

from flask import Blueprint, render_template, redirect, url_for, request
from .models import Post, db

main = Blueprint('main', __name__)

# Timeline route
@main.route('/home')
def home():
    posts = Post.query.order_by(Post.timestamp.desc()).all()  # Show newest posts first
    return render_template('home.html', posts=posts)

# New post submission route
@main.route('/post', methods=['POST'])
def post():
    username = request.form['username']
    content = request.form['content']

    # Create a new post
    new_post = Post(username=username, content=content)
    db.session.add(new_post)
    db.session.commit()

    return redirect(url_for('main.home'))
