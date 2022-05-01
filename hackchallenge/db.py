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
    tags = db.relationship("Tag", secondary=association_table, back_populates="foods")

    def __init__(self, **kwargs): # **kwargs - keyword arguments, a dictionary of key-value pairs
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

class Tag(db.Model):
    """
    Tag model
    """
    __tablename__="tags"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    color = db.Column(db.String, nullable=False)
    foods = db.relationship("Food", secondary=association_table, back_populates="tags")
    # a relationship in one direction -> a relationship in the other direction

    def __init__(self, **kwargs):
        """
        Initializes a Category object
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
