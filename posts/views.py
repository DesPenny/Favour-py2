from flask import render_template, g

from posts import app
from .database import session
from .models import Post

import mistune
from flask import request, redirect, url_for
#from flask.ext.login import login_required
#from flask.ext.login import current_user

from flask import flash
#from flask.ext.login import login_user, logout_user
#from werkzeug.security import check_password_hash
#from .models import User

@app.route("/")
#@app.route("/api/posts")
def posts():
    posts = session.query(Post)
    #posts = posts.order_by(Post.datetime.desc())
    posts = posts.all()
    return render_template("posts.html",
        posts=posts
    )
'''
@app.route("/")
@app.route("/page/<int:page>")
def posts(page=1, paginate_by=10):
    # Zero-indexed page
    page_index = page - 1

    count = session.query(Post).count()

    start = page_index * paginate_by
    end = start + paginate_by

    total_pages = (count - 1) / paginate_by + 1
    has_next = page_index < total_pages - 1
    has_prev = page_index > 0

    posts = session.query(Post)
    posts = posts.order_by(Post.datetime.desc())
    posts = posts[start:end]

    return render_template("posts.html",
        posts=posts,
        has_next=has_next,
        has_prev=has_prev,
        page=page,
        total_pages=total_pages
    )
'''
@app.route("/api/post/add", methods=["GET"])
#@login_required
def add_post_get():
    return render_template("add_post.html")
  

@app.route("/api/post/add", methods=["POST"])
#@login_required
def add_post_post():
    post = Post(
        title=request.form["title"],
        body=mistune.markdown(request.form["content"]),
        #author=current_user
    )
    session.add(post)
    session.commit()
    return redirect(url_for("posts"))

@app.route("/post/<postid>")
def post(postid=Post.id):
    post = session.query(Post).filter(Post.id == postid).first()
    return render_template(
        "single_post.html",
        post=post,
        postid=postid,
    )  
@app.route('/logout')
def logout():
    #logout_user()
    return redirect(url_for('posts'))