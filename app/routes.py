from flask import Blueprint, render_template, redirect, url_for, request
from .models import User, Post, Comment, db
from collections import Counter

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
            # Redirect to home after successful login
            return redirect(url_for('main.home'))
        else:
            # Redirect back to login on failure
            return redirect(url_for('main.login'))

    return render_template('login.html')

# Function to calculate trending topics based on post content
def get_trending_topics(posts, num_trends=5):
    words = []
    for post in posts:
        words.extend(post.content.lower().split())  # Collect all words from each post
    common_words = Counter(words).most_common(num_trends)  # Get the most common words
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