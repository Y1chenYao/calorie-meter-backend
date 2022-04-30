from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# association tables for instructors, students, and assignments
assoc_ins_table = db.Table(
    "ins_table",
    db.Model.metadata,
    db.Column("course_id", db.Integer, db.ForeignKey("course.id")),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"))
)

assoc_stu_table = db.Table(
    "stu_table",
    db.Model.metadata,
    db.Column("course_id", db.Integer, db.ForeignKey("course.id")),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"))
)


class Course(db.Model):
    __tablename__ = "course"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    instructors = db.relationship(
        "User", secondary=assoc_ins_table, back_populates="ins_courses")
    students = db.relationship(
        "User", secondary=assoc_stu_table, back_populates="stu_courses")
    assignments = db.relationship("Assignment", cascade="delete")

    def __init__(self, **kwargs):
        # initialize course object/entry
        self.code = kwargs.get("code", "")
        self.name = kwargs.get("name", "")

    def serialize(self):
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "assignments": [a.simple_serialize() for a in self.assignments],
            "instructors": [i.simple_serialize() for i in self.instructors],
            "students": [s.simple_serialize() for s in self.students]
        }

    def simple_serialize(self):
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name
        }


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    netid = db.Column(db.String, nullable=False)
    ins_courses = db.relationship(
        "Course", secondary=assoc_ins_table, back_populates="instructors")
    stu_courses = db.relationship(
        "Course", secondary=assoc_stu_table, back_populates="students")

    def __init__(self, **kwargs):
        # initialize user object/entry
        self.name = kwargs.get("name", "")
        self.netid = kwargs.get("netid", "")

    def serialize(self):
        course = []
        for c in self.ins_courses:
            course.append(c.simple_serialize())
        for c in self.stu_courses:
            course.append(c.simple_serialize())
        return {
            "id": self.id,
            "name": self.name,
            "netid": self.netid,
            "courses": course
        }

    def simple_serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "netid": self.netid
        }


class Assignment(db.Model):
    __tablename__ = "assignment"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    due_date = db.Column(db.Integer, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey(
        "course.id"), nullable=False)

    def __init__(self, **kwargs):
        # initialize assignment object/entry
        self.title = kwargs.get("title", "")
        self.due_date = kwargs.get("due_date")
        self.course_id = kwargs.get("course_id")

    def serialize(self):
        course = Course.query.filter_by(id=self.course_id).first()
        return {
            "id": self.id,
            "title": self.title,
            "due_date": self.due_date,
            "course": course.simple_serialize()
        }

    def simple_serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "due_date": self.due_date,
        }
