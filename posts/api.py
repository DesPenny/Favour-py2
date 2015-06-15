import json

from flask import request, redirect, Response, url_for, send_from_directory
from jsonschema import validate, ValidationError
from werkzeug.utils import secure_filename

import models
import decorators
from posts import app
from database import session
from utils import upload_path

# JSON Schema describing the structure of a post
post_schema = {
    "properties": {
        "title" : {"type" : "string"},
        "body": {"type": "string"}
    },
    "required": ["title", "body"]
}

@app.route("/api/posts", methods=["GET"])
@decorators.accept("application/json")
def posts_get():
    """ Get a list of posts """
    # Get the querystring arguments
    title_like = request.args.get("title_like")
    body_like = request.args.get("body_like")
    title_body = request.args.get("title_like") and request.args.get("body_like")
    # Get and filter the posts from the database
    posts = session.query(models.Post)
    if title_like and not body_like:
        posts = posts.filter(models.Post.title.contains(title_like))
    if body_like and not title_like:
        posts = posts.filter(models.Post.body.contains(body_like))
    if title_body:
      posts = posts.filter(models.Post.title.contains(title_like) & (models.Post.body.contains(body_like)))
    posts = posts.all()

    # Convert the posts to JSON and return a response
    data = json.dumps([post.as_dictionary() for post in posts])
    return Response(data, 200, mimetype="application/json")
  
@app.route("/api/posts/<int:id>", methods=["GET"])
@decorators.accept("application/json")
def post_get(id):
        """ Single post endpoint """
        # Get the post from the database
        post = session.query(models.Post).get(id)

        # Check whether the post exists
        # If not return a 404 with a helpful message
        if not post:
            message = "Could not find post with id {}".format(id)
            data = json.dumps({"message": message})
            return Response(data, 404, mimetype="application/json")

        # Return the post as JSON
        data = json.dumps(post.as_dictionary())
        return Response(data, 200, mimetype="application/json")
      
@app.route("/api/posts/<id>", methods=["DELETE"])
@decorators.accept("application/json")
def post_delete(id):
        # Single post endpoint 
        # Delete the post from the database
        post = session.query(models.Post).get(id)

        # Check whether the post exists
        # If not return a 404 with a helpful message
        if not post:
            message = "Could not find post with id {}".format(id)
            data = json.dumps({"message": message})
            return Response(data, 404, mimetype="application/json")
        session.delete(post)
        session.commit()
        # Return the post as JSON
        success = "Successfully deleted post"
        data = json.dumps({"message": success})
        return Response(data, 204, mimetype="application/json")
        # Convert the posts to JSON and return a response
        #data = json.dumps(post.as_dictionary())
        #return Response(data, 200, mimetype="application/json")
  
@app.route("/api/posts", methods=["POST"])
#@decorators.accept("application/json")
#@decorators.require("application/json")
def posts_post():
    """ Add a new post """
    data = request.json
    
    # Check that the JSON supplied is valid
    # If not you return a 422 Unprocessable Entity
    try:
        validate(data, post_schema)
    except ValidationError as error:
        data = {"message": error.message}
        return Response(json.dumps(data), 422, mimetype="application/json")
    
    # Add the post to the database
    post = models.Post(title=data["title"], body=data["body"])
    session.add(post)
    session.commit()

    # Return a 201 Created, containing the post as JSON and with the
    # Location header set to the location of the post
    data = json.dumps(post.as_dictionary())
    headers = {"Location": url_for("post_get", id=post.id)}
    return Response(data, 201, headers=headers,
                    mimetype="application/json")
  
  
@app.route("/api/posts/<id>", methods=["PUT"])
@decorators.accept("application/json")
@decorators.require("application/json")
def posts_edit(id):
    """ Editing a post """
    # Get the post from the database
    post = session.query(models.Post).get(id)

    # Check whether the post exists
    # If not return a 404 with a helpful message
    if not post:
        message = "Could not find post with id {}".format(id)
        data = json.dumps({"message": message})
        return Response(data, 404, mimetype="application/json")
    
    data = request.json
    
    # Check that the JSON supplied is valid
    # If not you return a 422 Unprocessable Entity
    try:
        validate(data, post_schema)
    except ValidationError as error:
        data = {"message": error.message}
        return Response(json.dumps(data), 422, mimetype="application/json")
    
    # Add the post to the database
    post.title=data["title"]
    post.body=data["body"]
    session.commit()
    
    data = json.dumps(post.as_dictionary())
    headers = {"Location": url_for("post_get", id=post.id)}
    return Response(data, 201, headers=headers,
                    mimetype="application/json")

@app.route("/uploads/<filename>", methods=["GET"])
def uploaded_file(filename):
    return send_from_directory(upload_path(), filename)

@app.route("/api/files", methods=["POST"])
@app.route("/api/post/add", methods=["POST"])
@decorators.require("multipart/form-data")
#@decorators.accept("application/json")
def file_post():
    file = request.files["file"]
    if not file:
        data = {"message": "Could not find file data or filetype not permitted"}
        return Response(json.dumps(data), 422, mimetype="application/json")

    filename = secure_filename(file.filename)
    file.save(upload_path(filename))
    #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return redirect(url_for('posts', filename=filename))
    #db_file = models.File(filename=filename)
    #session.add(db_file)
    #session.commit()
    #file.save(upload_path(filename))

    #data = db_file.as_dictionary()
    #return Response(json.dumps(data), 201, mimetype="application/json")
'''
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
'''  