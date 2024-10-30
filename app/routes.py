from flask import Blueprint, render_template, redirect, url_for, request
from .models import User, Post, Comment, db
from collections import Counter
from datetime import datetime, timedelta
from flask_login import login_user, login_required, current_user

from flask_login import login_user

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
            login_user(user)  # Log the user in
            return redirect(url_for('main.view_account'))
        else:
            # Redirect back to login on failure
            return redirect(url_for('main.login'))

    return render_template('login.html')

# Function to calculate trending topics based on post content
def get_trending_topics(posts, num_trends=5):
    words = []
    for post in posts:
        # Split the content into words and add to the list
        words.extend(post.content.lower().split())
    # Get the most common words from all posts
    common_words = Counter(words).most_common(num_trends)
    # Extract just the words for trending topics
    trending_topics = [word for word, _ in common_words]
    return trending_topics

# Timeline route (Home page) with trending topics
@main.route('/home')
def home():
    search_query = request.args.get('query')
    if search_query:
        posts = Post.query.filter(
            (Post.username.contains(search_query)) |
            (Post.content.contains(search_query))
        ).order_by(Post.timestamp.desc()).all()
    else:
        posts = Post.query.order_by(Post.timestamp.desc()).all()
    
    # Calculate trending topics from the posts
    trending_topics = get_trending_topics(posts)
    
    return render_template('home.html', posts=posts, search_query=search_query, trending_topics=trending_topics)

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

# Route to like a post
@main.route('/like_post/<int:post_id>', methods=['POST'])
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.like_count += 1  # Increment like count
    db.session.commit()
    return redirect(url_for('main.home'))

# Route to add a comment
@main.route('/add_comment/<int:post_id>', methods=['POST'])
def add_comment(post_id):
    post = Post.query.get_or_404(post_id)
    username = request.form['username']
    content = request.form['content']

    # Add new comment
    new_comment = Comment(post_id=post_id, username=username, content=content)
    db.session.add(new_comment)
    db.session.commit()
    return redirect(url_for('main.home'))

# View Account Route
@main.route('/account')
@login_required  # Ensure only logged-in users can access this route
def view_account():
    user = current_user  # Get the currently logged-in user
    user_posts = Post.query.filter_by(username=user.username).all()  # Fetch user's posts

    return render_template('account.html', user=user, posts=user_posts)

# Delete post route
@main.route('/delete_post/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('main.home'))

# Index Route (Main landing page)
@main.route('/')
def index():
    return render_template('index.html')
