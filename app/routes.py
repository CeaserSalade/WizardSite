from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, current_user
from .models import User, Post, Comment, db
from collections import Counter
from datetime import datetime, timedelta

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
            return redirect(url_for('main.home'))
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
@login_required  # Ensure only logged-in users can post
def post():
    content = request.form['content']

    # Create a new post using the logged-in user's username
    new_post = Post(username=current_user.username, content=content)
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
@login_required  # Ensure only logged-in users can comment
def add_comment(post_id):
    post = Post.query.get_or_404(post_id)
    content = request.form['content']

    # Add new comment using the logged-in user's username
    new_comment = Comment(post_id=post_id, username=current_user.username, content=content)
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

# View Replies Route
@main.route('/account/replies')
@login_required
def view_replies():
    user = current_user
    user_replies = Comment.query.filter_by(username=user.username).order_by(Comment.timestamp.desc()).all()
    return render_template('replies.html', user=user, replies=user_replies)

# Delete post route
@main.route('/delete_post/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('main.home'))

@main.route('/profile/<string:username>')
def view_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    user_posts = Post.query.filter_by(username=user.username).order_by(Post.timestamp.desc()).all()  # Fetch the user's posts

    return render_template('profile.html', user=user, posts=user_posts)

@main.route('/follow/<int:user_id>')
@login_required
def follow(user_id):
    user = User.query.get_or_404(user_id)
    if user == current_user:
        flash("You cannot follow yourself!", "warning")
        return redirect(url_for('main.view_account', user_id=user_id))
    current_user.follow(user)
    db.session.commit()
    flash(f"You are now following {user.username}", "success")
    return redirect(url_for('main.view_account', user_id=user_id))

@main.route('/unfollow/<int:user_id>')
@login_required
def unfollow(user_id):
    user = User.query.get_or_404(user_id)
    if user == current_user:
        flash("You cannot unfollow yourself!", "warning")
        return redirect(url_for('main.view_account', user_id=user_id))
    current_user.unfollow(user)
    db.session.commit()
    flash(f"You have unfollowed {user.username}", "info")
    return redirect(url_for('main.view_account', user_id=user_id))

# Index Route (Main landing page)
@main.route('/')
def index():
    return render_template('index.html')
