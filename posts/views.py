from flask import render_template, g

from posts import app
from posts import api
from .database import session
from .models import Post
import decorators
import mistune
from flask import request, redirect, Response, url_for, send_from_directory
#from flask.ext.login import login_required
#from flask.ext.login import current_user

from flask import flash
#from flask.ext.login import login_user, logout_user
#from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
#from .models import User
from utils import upload_path
from PIL import Image
#from thumbnails import get_thumbnail


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
    try:
        post = Post(
        title=request.form["title"],
        body=mistune.markdown(request.form["content"]),
        #author=current_user
        )
        session.add(post)
        session.commit()

        file_post()
        return redirect(url_for("posts"))
    except RequestEntityTooLarge as e:
      return e

@app.route("/post/<postid>")
def post(postid=Post.id):
    post = session.query(Post).filter(Post.id == postid).first()
    return render_template(
        "single_post.html",
        post=post,
        postid=postid,
    )  
  
@app.route("/post/<postid>/edit", methods=["GET"])
#@login_required
def edit_post_get(postid):
    post = session.query(Post).get(postid)
    #if not post.author_id==current_user.id:
    #  raise AssertionError("Not Allowed")
    post = session.query(Post).get(postid)
    return render_template("edit_post.html", post=post,postid=postid)
'''
@app.route("/post/<postid>/edit", methods=["POST"])
#@login_required
def edit_post(postid):
    post = session.query(Post).get(postid)
    #if not post.author_id==current_user.id:
    #  raise AssertionError("Not Allowed")
    title = request.form["title"]
    #content = mistune.markdown(request.form["content"])
    body = request.form["body"]
    session.query(Post).filter_by(id=postid).update(
        {"title": title, "body": body}
    )
    session.commit()
    return redirect(url_for("posts"))
'''
@app.route("/post/<int:id>/edit", methods=["GET", "POST"])
#@login_required
def edit_post(id):
    if request.method == "POST":
        post = session.query(Post).get(id)
        post.title = request.form["title"]
        post.body = request.form["content"]
        session.add(post)
        session.commit()
        return redirect(url_for("posts"))

    post = session.query(Post).get(id)
    return render_template("edit_post.html", post=post)
  
@app.route("/post/<postid>/delete", methods=["POST"])
#@login_required
def delete_post(postid):
    post = session.query(Post).get(postid)
    #if not post.author_id==current_user.id:
    #  raise AssertionError("Not Allowed")
    session.query(Post).filter_by(id=postid).delete()
    session.commit()
    return redirect(url_for("posts"))
  
@app.route('/logout')
def logout():
    #logout_user()
    return redirect(url_for('posts'))
  
@app.route("/uploads/<filename>", methods=["GET"])
def uploaded_file(filename):
    filename = 'http://127.0.0.1:8080/uploads/' + filename
    return send_from_directory(upload_path(), filename)

def gen_thumbnail(filename):
	  height = width = 50
	  original = Image.open(upload_path(), filename)
	  thumbnail = original.resize((width, height))
	  thumbnail.save(upload_path('thumb_'+filename))

def file_post():
    file = request.files["file"]
    if not file:
        data = {"message": "Could not find file data or filetype not permitted"}
        return Response(json.dumps(data), 422, mimetype="application/json")

    #filename = secure_filename(file.filename)
    response = session.query(Post.id).order_by('-id').first()
    filename = secure_filename(str(response[0]))
    file.save(upload_path(filename))
    gen_thumbnail(filename)
    #thumbnail = thumbnails.get_thumbnail(upload_path(filename), '50x50', crop='center')
    #thumbnail.save(upload_path('thumb_'+filename))
    return redirect(url_for('posts', filename=filename))