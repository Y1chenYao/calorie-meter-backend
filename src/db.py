from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# association tables for foods and tags
assoc_table = db.Table(
    "association",
    db.Model.metadata,
    db.Column("food_id", db.Integer, db.ForeignKey("food.id")),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id"))
)


class Food(db.Model):
    __tablename__ = "food"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    calorie = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String, nullable=False)
    # to be debugged
    tags = db.relationship("Tag", secondary=assoc_table, back_populates="foods")

    def __init__(self, **kwargs):
        # initialize food object/entry
        self.name = kwargs.get("name", "")
        self.description = kwargs.get("description", "")
        self.image = kwargs.get("image", "")
        self.calorie = kwargs.get("calorie",)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "calorie": self.calorie,
            "image": self.image,
            "tags": [t.simple_serialize() for t in self.tags],
        }

    def simple_serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "calorie": self.calorie,
            "image": self.image
        }


class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)

    # Stored as a hex string
    color = db.Column(db.String, nullable=False)
    foods = db.relationship("Food", secondary=assoc_table, back_populates="tags")

    def __init__(self, **kwargs):
        # initialize user object/entry
        self.name = kwargs.get("name", "")
        self.color = kwargs.get("color", "")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "color": self.color,
            "foods": [f.simple_serialize() for f in self.foods],
        }

    def simple_serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "color": self.color,
        }
