from datetime import datetime
import string
import re
import random
from PIL import Image
import os
from mimetypes import guess_extension, guess_type
from io import BytesIO
import io
import datetime
import boto3
import base64
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Table is like a lightweighted version of Model
association_table = db.Table(
    "association",
    db.Column("task_id", db.Integer, db.ForeignKey("foods.id")),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id"))
)

# implement database model classes


class Food(db.Model):
    """
    Food model
    Has a many-to-many relationship with the Tag model
    """
    __tablename__ = "foods"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    tags = db.relationship(
        "Tag", secondary=association_table, back_populates="foods")

    def __init__(self, **kwargs):  # **kwargs - keyword arguments, a dictionary of key-value pairs
        """
        initialize Task object/entry
        """
        self.name = kwargs.get("name")
        self.description = kwargs.get("description", "")
        self.calories = kwargs.get("calories", 0)

    def serialize(self):
        """
        Serializes Task object
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "calories": self.calories,
            "tags": [c.simple_serialize() for c in self.tags]
        }

    def simple_serialize(self):
        """
        Simple serializes a food object
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "calories": self.calories,
        }


class Tag(db.Model):
    """
    Tag model
    """
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    color = db.Column(db.String, nullable=False)
    foods = db.relationship(
        "Food", secondary=association_table, back_populates="tags")
    # a relationship in one direction -> a relationship in the other direction

    def __init__(self, **kwargs):
        """
        Initializes a Tag object
        """
        self.name = kwargs.get("name", "")
        self.color = kwargs.get("color", "")

    def simple_serialize(self):
        """
        Simple serializes a Tag object
        """
        return {
            "id": self.id,
            "name": self.name,
            "color": self.color,
        }

    def serialize(self):
        """
        Simple serializes a Tag object
        """
        return {
            "id": self.id,
            "name": self.name,
            "color": self.color,
            "foods": [c.simple_serialize() for c in self.foods]
        }


db = SQLAlchemy()

EXTENSIONS = ["png", "gif", "jpg", "jpeg"]
BASE_DIR = os.getcwd()
S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")
S3_BASE_URL = f"https://{S3_BUCKET_NAME}.s3.us-east-1.amazonaws.com"


class Asset(db.Model):
    """
    Asset model
    """
    __tablename__ = "assets"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    base_url = db.Column(db.String, nullable=True)
    salt = db.Column(db.String, nullable=False)
    extension = db.Column(db.String, nullable=False)
    width = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, **kwargs):
        """
        Initializes an Asset object
        """
        self.create(kwargs.get("image_data"))

    def serialize(self):
        """
        Serializes an Asset object
        """
        return {
            "url": f"{self.base_url}/{self.salt}.{self.extension}",
            "created_at": str(self.created_at())
        }

    def create(self, image_data):
        """
        Given an image in base64 form, does the following:
        1) Rejects the image if it is not a supoprt filetype
        2) Generates a random string for the image filename
        3) Decodes the image and attempts to upload it to tAWS
        """

        try:
            ext = guess_extension(guess_type(image_data)[0])[1:]

            # only accept supported file extensions
            if ext not in EXTENSIONS:
                raise Exception(f"Unsupported file type:{ext}")

            # secure way of generating a random string for image filename
            salt = "".join(
                random.SystemRandom().choice(
                    string.ascii_letters + string.digits
                )
                for _ in range(16)
            )

            # remove header of base64 string
            img_str = re.sub("^data:image/.+;base64,", "", image_data)
            img_data = base64.b64decode(img_str)
            img = Image.open(BytesIO(img_data))

            self.base_url = S3_BASE_URL
            self.salt = salt
            self.extension = ext
            self.width = img.width
            self.height = img.height
            self.created_at = datetime.datetime.now()

            img_filename = f"{self.salt}.{self.extension}"
            self.upload(img, img_filename)
        except Exception as e:
            print(f"Error when creating image: {e}")

    def upload(self, img, img_filename):
        """
        ATtempts to upload the image to the specified S3 bucket.
        """

        try:
            # save image temporarily on server
            img_temploc = f"{BASE_DIR}/{img_filename}"

            img.save(img_temploc)

            # upload the image to S3
            s3_client = boto3.client("s3")
            s3_client.upload_file(img_temploc, S3_BUCKET_NAME, img_filename)

            # make S3 image url public
            s3_resource = boto3.resource("s3")
            object_acl = s3_resource.ObjectAcl(S3_BUCKET_NAME, img_filename)
            object_acl.put(ACL="public-read")

            # remove image from server
            os.remove(img_temploc)
        except Exception as e:
            print(f"Error when uploading image: {e}")
