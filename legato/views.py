from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Post, User, Comment, Like, Dislike
from . import db
from .helpers import from_now, hot
from datetime import datetime

# Create Blueprint object to handle all views routes
views = Blueprint("views", __name__)


@views.route("/")
@views.route("/index")
@login_required
def index():
    '''Show posts in the home page'''

    # Search returns None if there is no search
    search = request.args.get("search")
    # Query comments
    comments = Comment.query.all()
    # Fetch current utc time
    now = datetime.utcnow()

    if search:
        # Return a list of Post objects containing search in body or title
        posts = Post.query.filter(Post.title.contains(
            search) | Post.text.contains(search)).all()

    else:
        # Query all posts
        posts = Post.query.all()

    # Loop through the posts list of post objects
    for post in posts:
        # Create arguments to be used by the hot function
        date = post.date_created
        ups = len(post.likes)
        downs = len(post.dislikes)
        # Call hot and store result in new .hot_score attribute to post
        post.hot_score = hot(ups, downs, date)

    # Sorted sorts in reverse order a list of Post objects by the key parameter: a lamba function having post.hot_score as argument
    sorted_posts = sorted(posts, key=lambda post: post.hot_score, reverse=True)

    # Loop through the sorted_posts list
    for post in sorted_posts:
        # Create argument to be used by the from_now function
        time_diff = now - post.date_created
        # Call from_now and store result in new .time_passed attribute to post
        post.time_passed = from_now(time_diff)

    # Loop through the comments list
    for comment in comments:
        time_diff = now - comment.date_created
        comment.time_passed = from_now(time_diff)

    return render_template("index.html", user=current_user, posts=sorted_posts)


@views.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():
    '''Create a new post'''

    if request.method == "POST":
        # Get post title and text from the form
        title = request.form.get("title")
        text = request.form.get("text")

        if not title:
            flash("Title cannot be empty", category="error")
        if not text:
            flash("Post cannot be empty", category="error")
        else:
            # Add post to database
            post = Post(title=title, text=text, author_id=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash("Post created", category="success")
            return redirect(url_for("views.index"))

    return render_template('create_post.html', user=current_user)


@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    '''Delete a personal post'''

    # Query post filtering by the id number in the url
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash("Post does not exist", category="error")
    elif current_user.id != post.author_id:
        flash("You do not have permission to delete this post", category="error")
    else:
        # Delete post from database
        db.session.delete(post)
        db.session.commit()
        flash("post deleted", category="success")

    return redirect(url_for("views.index"))


@views.route("/posts/<username>")
@login_required
def posts(username):
    '''Show user's personal posts'''

    # Query user filtering by the username in the url
    user = User.query.filter_by(username=username).first()

    if not user:
        flash("No user with that username exists", category="error")
        return redirect(url_for("views.index"))

    # Store only the posts from the current user in the posts variable
    posts = user.posts
    return render_template("posts.html", user=current_user, posts=posts, username=username)


@views.route("/create-comment/<post_id>", methods=["POST"])
def create_comment(post_id):
    '''Comment posts'''
    # Get comment text from the form
    text = request.form.get("text")

    if not text:
        flash("Comment cannot be empty", category="error")
    else:
        # Query post by the comment's post_id in the url
        post = Post.query.filter_by(id=post_id)
        if post:
            # Add post to database
            comment = Comment(
                text=text, author_id=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash("Post does not exist", category="error")

    return redirect(url_for("views.index"))


@views.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    '''Delete a personal comment'''
    # Query comment filtering by the comment id number in the url
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash("Comment does not exist", category="error")
    # Only allow author of the comment or author of the post commented to delete comment
    elif current_user.id != comment.author_id and current_user.id != comment.post.author_id:
        flash("You do not have permission to delete this comment", category="error")
    else:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for("views.index"))


@views.route("/like-post/<post_id>", methods=["GET"])
@login_required
def like(post_id):
    '''Like a post'''

    # Query post filtering by the post_id in the url
    post = Post.query.filter_by(id=post_id).first()
    # Query like filtering by the imported current user and the post_id in the url
    like = Like.query.filter_by(
        author_id=current_user.id, post_id=post_id).first()
    # Query dislike filtering by the imported current user and the post_id in the url
    dislike = Dislike.query.filter_by(
        author_id=current_user.id, post_id=post_id).first()

    if not post:
        flash("Post does not exist", category="error")
    # If we haven't cast a vote, add a like
    elif not like and not dislike:
        like = Like(author_id=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()
    # If we already disliked, add a like and remove a dislike
    elif not like and dislike:
        like = Like(author_id=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.delete(dislike)
        db.session.commit()
    # If we already liked, remove the like
    else:
        db.session.delete(like)
        db.session.commit()

    return redirect(url_for("views.index"))


@views.route("/dislike-post/<post_id>", methods=["GET"])
@login_required
def dislike(post_id):
    '''Dislike a post'''

    # Query post filtering by the post_id in the url
    post = Post.query.filter_by(id=post_id).first()
    # Only allow author of the comment or author of the post commented to delete comment
    like = Like.query.filter_by(
        author_id=current_user.id, post_id=post_id).first()
    # Query dislike filtering by the imported current user and the post_id in the url
    dislike = Dislike.query.filter_by(
        author_id=current_user.id, post_id=post_id).first()

    if not post:
        flash("Post does not exist", category="error")
    # If we haven't cast a vote, add a dislike
    elif not dislike and not like:
        dislike = Dislike(author_id=current_user.id, post_id=post_id)
        db.session.add(dislike)
        db.session.commit()
    # If we already liked, add a dislike and remove a like
    elif not dislike and like:
        dislike = Dislike(author_id=current_user.id, post_id=post_id)
        db.session.add(dislike)
        db.session.delete(like)
        db.session.commit()
    # If we already disliked, remove the dislike
    else:
        db.session.delete(dislike)
        db.session.commit()

    return redirect(url_for("views.index"))
