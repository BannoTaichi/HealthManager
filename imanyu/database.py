from datetime import datetime
import pytz
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    weight = db.Column(db.Float, nullable=True)
    height = db.Column(db.Float, nullable=True)
    activity_level = db.Column(db.Float, nullable=True)

    def get_id(self):
        return str(self.id)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.String(300), nullable=False)
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now(pytz.timezone("Asia/Tokyo"))
    )


class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    base_amount = db.Column(db.Float, nullable=True)
    protein = db.Column(db.Float, nullable=True)
    carbs = db.Column(db.Float, nullable=True)
    fat = db.Column(db.Float, nullable=True)
    vitamins = db.Column(db.Float, nullable=True)
    minerals = db.Column(db.Float, nullable=True)


class MealLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    meal_id = db.Column(db.Integer, db.ForeignKey("meal.id"), nullable=False)
    amount = db.Column(db.Float, nullable=True)
    date = db.Column(
        db.DateTime, nullable=False, default=datetime.now(pytz.timezone("Asia/Tokyo"))
    )
    user = db.relationship("User", backref="meal_logs")
    meal = db.relationship("Meal", backref="meal_logs")


class Stretch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Float, nullable=False)
    base_reps = db.Column(db.Integer, nullable=False)
    calories = db.Column(db.Float, nullable=False)


class StretchLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    stretch_id = db.Column(db.Integer, db.ForeignKey("stretch.id"), nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    date = db.Column(
        db.DateTime, nullable=False, default=datetime.now(pytz.timezone("Asia/Tokyo"))
    )
    user = db.relationship("User", backref="stretch_logs")
    stretch = db.relationship("Stretch", backref="stretch_logs")
