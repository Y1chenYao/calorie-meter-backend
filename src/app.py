import json

from db import db
from db import Food
from db import Tag
from flask import Flask
from flask import request
from dotenv import dotenv_values

import os

# define db filename
db_filename = "calorie.db"
app = Flask(__name__)

# setup config
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_filename}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True


S3_BUCKET_NAME = dotenv_values(".env")["S3_BUCKET_NAME"]

# initialize app
db.init_app(app)
with app.app_context():
    db.create_all()


# generalized response formats
def success_response(data, code=200):
    return json.dumps(data), code


def failure_response(message, code=404):
    return json.dumps({"error": message}), code


# -- TASK ROUTES ------------------------------------------------------


@app.route("/")
def hello_world():
    """
    Endpoint for printing "Hello World!"
    """
    return "Hello " + os.environ.get("NAME") + "!"


@app.route("/foods/")
def get_foods():
    """
    Endpoint for getting all foods
    """
    return success_response({"foods": [t.serialize() for t in Food.query.all()]})


@app.route("/foods/", methods=["POST"])
def create_food():
    """
    Endpoint for creating a new food
    """
    body = json.loads(request.data)

    # filter bad input
    if "name" not in body or body.get("name") == "":
        return json.dumps({"error": "bad request: no name"}), 400
    if "description" not in body or body.get("description") == "":
        return json.dumps({"error": "bad request: no description"}), 400
    if "calories" not in body or (not isinstance(body.get("calories"), int)) or (body.get("calories") < 0):
        return json.dumps({"error": "bad request: calories must be nonnegative integer"}), 400

    new_food = Food(name=body.get("name"), description=body.get(
        "description"), calories=body.get("calories"), image_url=body.get("image_url"))
    db.session.add(new_food)
    db.session.commit()
    return success_response(new_food.serialize(), 201)


@app.route("/foods/<int:food_id>/")
def get_food_by_id(food_id):
    """
    Endpoint for getting a food by id
    """
    food = Food.query.filter_by(id=food_id).first()
    if food is None:
        return failure_response("Food not found")
    return success_response(food.serialize())


@app.route("/foods/<food_name>/")
def get_food_by_name(food_name):
    """
    Endpoint for getting foods by name
    Return a list of foods, since multiple entries can share the same name
    """
    return success_response({"foods": [t.serialize() for t in Food.query.filter_by(name=str(food_name))]})


@app.route("/foods/<int:food_id>/", methods=["POST"])
def update_food(food_id):
    """
    Endpoint for updating a food by id
    """
    body = json.loads(request.data)
    food = Food.query.filter_by(id=food_id).first()
    if food is None:
        return failure_response("Food not find")
    # if calories is nonempty and is not a nonnegative integer, return an error message
    if (body.get("calories") is not None) and ((not isinstance(body.get("calories"), int)) or (body.get("calories") < 0)):
        return json.dumps({"error": "bad request: calories must be nonnegative integer"}), 400
    # if user input is not specified, default to what it was previously
    food.name = body.get("name", food.name)
    food.description = body.get("description", food.description)
    food.calories = body.get("calories", food.calories)
    food.image_url = body.get("image_url", food.image_url)
    db.session.commit()
    return success_response(food.serialize())


@app.route("/foods/getimage/<int:food_id>/")
def get_food_image(food_id):
    """
    Endpoint for getting the image of a food by the id
    """
    food = Food.query.filter_by(id=food_id).first()
    return success_response({"image_url": f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/rice.jpeg"})


@app.route("/foods/<int:food_id>/", methods=["DELETE"])
def delete_food(food_id):
    """
    Endpoint for deleting a food by id
    """
    food = Food.query.filter_by(id=food_id).first()
    if food is None:
        return failure_response("Food not exist")
    db.session.delete(food)
    db.session.commit()
    return success_response(food.serialize())


@app.route("/tags/")
def get_tags():
    """
    Endpoint for getting all tags
    """
    return success_response({"tags": [t.serialize() for t in Tag.query.all()]})


@app.route("/tags/", methods=["POST"])
def create_tag():
    """
    Endpoint for creating a tag
    """
    body = json.loads(request.data)
    if "name" not in body or body.get("name") == "":
        return json.dumps({"error": "bad request: no name"}), 400
    if "color" not in body or body.get("color") == "":
        return json.dumps({"error": "bad request: no color"}), 400
    new_tag = Tag(name=body.get("name"), color=body.get("color"))
    db.session.add(new_tag)
    db.session.commit()
    return success_response(new_tag.serialize(), 201)


@app.route("/tags/<int:tag_id>/")
def get_tag_by_id(tag_id):
    """
    Endpoint for getting a tag by id
    """
    tag = Tag.query.filter_by(id=tag_id).first()
    if tag is None:
        return failure_response("Tag not exist")
    return success_response(tag.serialize())


@app.route("/tags/<tag_name>/")
def get_tag_by_name(tag_name):
    """
    Endpoint for getting tag by name
    Return a list of tag whose name is the same as the name given
    If no tags are matched, return an EMPTY LIST
    If exactly 1 tag is matched, return a LIST OF ONE ELEMENT
    """
    return success_response({"tags": [t.serialize() for t in Tag.query.filter_by(name=str(tag_name))]})


@app.route("/foods/<int:food_id>/add/", methods=["POST"])
def add_tag_to_food(food_id):
    """
    Endpoint for adding a tag to food
    """
    body = json.loads(request.data)
    if "tag_id" not in body or body.get("tag_id") == "":
        return json.dumps({"error": "bad request: no tag_id"}), 400
    tag_id = body.get("tag_id")
    tag = Tag.query.filter_by(id=tag_id).first()
    if tag is None:
        return failure_response("Tag not exist")
    food = Food.query.filter_by(id=food_id).first()
    if food is None:
        return failure_response("Food not found")
    food.tags.append(tag)
    db.session.commit()
    return success_response(food.serialize())


@app.route("/tags/<int:tag_id>/", methods=["DELETE"])
def delete_tag(tag_id):
    """
    Endpoint for deleting a tag by id
    """
    tag = Tag.query.filter_by(id=tag_id).first()
    if tag is None:
        return failure_response("Tag not exist")
    db.session.delete(tag)
    db.session.commit()
    return success_response(tag.serialize())


@app.route("/upload/", methods=["POST"])
def upload():
    """
    Endpoint for uploading an image to AWS given its base64 form,
    then storing/returning the URL of that image
    """
    body = json.loads(request.data)
    image_data = body.get("image_data")
    if image_data is None:
        return failure_response("No base64 image to be found!")

    # create new Asset object
    asset = Asset(image_data=image_data)
    db.session.add(asset)
    db.session.commit()
    return success_response(asset.serialize(), 201)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
