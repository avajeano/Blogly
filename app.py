"""Blogly application."""

from flask import Flask, render_template, request, session, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "123"
debug = DebugToolbarExtension(app)

app.app_context().push()
connect_db(app)

@app.route('/')
def root():
    """Redirects to list of users."""
    return redirect("/users")

@app.route('/users')
def list_users():
    """Show list of all users in db."""
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/<int:user_id>')
def show_user(user_id):
    """Show details about a single user."""
    user = User.query.get_or_404(user_id)
    return render_template('details.html', user=user)

@app.route('/new_user', methods=["GET"])
def new_user_form():
    "Shows the new user form."
    return render_template('new_user.html')

@app.route('/new_user', methods=["POST"])
def create_user():
    """Handle the new user form."""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"] or None

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>/edit')
def edit_user_form(user_id):
    """Shows the edit user form."""
    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def handle_edit_user_form(user_id):
    """Handle the edit user form."""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"]

    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def handle_delete_user(user_id):
    """Deletes the user."""
    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
"""Post routes"""

@app.route('/users/<int:user_id>/posts_new')
def user_post_form(user_id):
    """Shows the user post form."""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('posts_new.html', user=user, tags=tags)

@app.route('/users/<int:user_id>/posts_new', methods=["POST"])
def handle_new_post(user_id):
    """Handle the user new post form."""
    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")] 
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(title=request.form['post_title'],
                    content=request.form['post_content'],
                    user=user,
                    tags=tags)
    
    db.session.add(new_post)
    db.session.commit()
    return redirect("/users")

@app.route('/posts/<post_id>')
def post_details(post_id):
    """Show the details for the post."""
    post = Post.query.get_or_404(post_id)
    return render_template('posts.html', post=post)

@app.route('/posts/<post_id>/edit')
def edit_post(post_id):
    """Show the edit post form."""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('edit_post.html', post=post, tags=tags)

@app.route('/posts/<post_id>/edit', methods=["POST"])
def hanlde_edit_post(post_id):
    """Handle the edit post form."""
    post = Post.query.get_or_404(post_id)
    post.title = request.form["post_title"]
    post.content = request.form["post_content"]

    tags_id = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tags_id)).all()

    db.session.add(post)
    db.session.commit()
    return redirect(f"/tags")

@app.route('/posts/<post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Delete post."""
    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    return redirect("/users")

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
"""Tag routes"""

@app.route('/tags')
def view_tags():
    """Shows list of all tags in db."""
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)

@app.route('/tags_new')
def new_tag_form():
        """Shows the new tag form."""
        posts = Post.query.all()
        return render_template('tags_new.html')

@app.route('/tags_new', methods=["POST"])
def create_tag():
    """Handle the new tag form."""
    tag_name = request.form["tag_name"]

    new_tag = Tag(tag_name=tag_name)
    db.session.add(new_tag)
    db.session.commit()

    return redirect("/tags")

@app.route('/tags/<tag_id>')
def show_tag_details(tag_id):
    """Show corresponding posts to a single tag."""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag_details.html', tag=tag)

@app.route('/tags/<tag_id>/edit')
def edit_tag(tag_id):
    """Show the edit tag form."""
    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('edit_tag.html', tag=tag, posts=posts)

@app.route('/tags/<tag_id>/edit', methods=["POST"])
def handle_edit_tag(tag_id):
    """Handle the edit tag form."""
    tag = Tag.query.get_or_404(tag_id)
    tag.tag_name = request.form["tag_name"]
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()
    return redirect ("/tags")

@app.route('/tags/<tag_id>/delete', methods=["POST"])
def handle_delete_tag(tag_id):
    """Deletes the tag."""
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.delete(tag)
    db.session.commit()

    return redirect("/tags")