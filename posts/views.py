from flask import render_template, g
from flask.ext.images import Images, resized_img_src
from posts import app
from posts import api
from .forms import RegistrationForm
from .database import session
from .models import Post
import decorators
import mistune
from flask import request, redirect, Response, url_for, send_from_directory
from flask.ext.login import login_required
from flask.ext.login import current_user
from flask.ext.wtf import Form
from flask import flash
from flask.ext.login import login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from .models import User
from utils import upload_path
from PIL import Image
from .email import send_email


#from thumbnails import get_thumbnail
app.secret_key = 'monkey'
app.debug = True
Images(app)
print app.root_path
'''
@app.route("/")
#@app.route("/api/posts")
def posts():
    posts = session.query(Post)
    postid = session.query(Post.id)
    posts = posts.order_by(Post.datetime.desc())
    posts = posts.all()
    return render_template("posts.html",
        posts=posts,
        
    
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

@app.route("/api/post/add", methods=["GET"])
@login_required
def add_post_get():
    return render_template("add_post.html")
  

@app.route("/api/post/add", methods=["POST"])
@login_required
def add_post_post():
    try:
        post = Post(
        title=request.form["title"],
        body=mistune.markdown(request.form["content"]),
        author=current_user
        )
        session.add(post)
        session.commit()
    
        file_post(post)
        return redirect(url_for("posts"))
    except RequestEntityTooLarge as e:
      return e

@app.route("/post/<postid>")
def post(postid=Post.id):
    post = session.query(Post).filter(Post.id == postid)
    return render_template(
        "single_post.html",
        post=post,
        
        
    )  
  
@app.route("/post/<postid>/edit", methods=["GET"])
@login_required
def edit_post_get(postid):
    post = session.query(Post).get(postid)
    print post
    if not post.author_id==current_user.id:
      raise AssertionError("Not Allowed")
    #post = session.query(Post).get(postid)
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
@app.route("/post/<int:id>/edit", methods=["POST"])
@login_required
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
  
@app.route("/post/<int:id>/delete", methods=["GET","POST"])
#@login_required
def delete_post(id):
    post = session.query(Post).get(id)
    #print post
    #if not post.author_id==current_user.id:
     # raise AssertionError("Not Allowed")
    #session.query(Post).filter_by(post).delete()
    session.delete(post)
    session.commit()
    return redirect(url_for('posts'))
    
  
@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('posts'))
    
@app.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html")
    
@app.route("/login", methods=["POST"])
def login_post():
    email = request.form["email"]
    password = request.form["password"]
    user = session.query(User).filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
    #if not user:
        flash("Incorrect username or password", "danger")
        return redirect(url_for("login_get"))

    login_user(user)
    return redirect(request.args.get('next') or url_for("posts"))
    
@app.route('/signup', methods=['GET' , 'POST'])
def signup():
    form=RegistrationForm()
    if request.method == 'POST':
        user = User(name=form.name.data, email=form.email.data, password=generate_password_hash(form.password.data))
        session.add(user)
        session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm your Account', 'email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you.')
        return redirect(url_for('posts'))
    return render_template('signup.html')  
    
@app.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('posts'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('posts'))
  
#@app.route("/uploads/<filename>", methods=["GET"])
#def uploaded_file(filename):
#    return send_from_directory(upload_path(), filename)

def gen_thumbnail(filename):
	  height = width = 50
	  original = Image.open(upload_path(filename))
	  thumbnail = original.resize((width, height))
	  thumbnail.save(upload_path('thumb_'+filename))

def file_post(post):
    file = request.files["file"]
    if not file:
        data = {"message": "Could not find file data or filetype not permitted"}
        return Response(json.dumps(data), 422, mimetype="application/json")

    #filename = secure_filename(file.filename)
    
    file.save(upload_path(post.main_image()))
    #gen_thumbnail(filename)
    #thumbnail = thumbnails.get_thumbnail(upload_path(filename), '50x50', crop='center')
    #thumbnail.save(upload_path('thumb_'+filename))
    #return send_from_directory(upload_path(), filename)