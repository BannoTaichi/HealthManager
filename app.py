from flask import Flask, render_template, request, redirect, session, url_for
import os
from flask_login import LoginManager, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from database import db, User, Post, MealLog, StretchLog
from model import (
    calc_nutrient_from_table,
    calc_total_nutrients,
    calc_burned_calories,
    get_recent_logs,
)
from datetime import datetime, timedelta
import collections, pytz
import pandas as pd

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
app.config["SECRET_KEY"] = os.urandom(24)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


@app.route("/")
def home():
    return redirect("/signup")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect("/login")
    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = db.session.query(User).filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            login_user(user)
            return redirect("/display_log")
    return render_template("login.html")


@app.route("/index", methods=["GET"])
@login_required
def index():
    user_id = session.get("user_id")
    user = db.session.get(User, user_id)
    posts = db.session.query(Post).filter_by(user_id=user_id).all()
    return render_template("index.html", posts=posts, user=user)


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    user_id = session.get("user_id")
    user = db.session.get(User, user_id)
    if request.method == "POST":
        age = request.form["age"]
        height = request.form["height"]
        weight = request.form["weight"]
        sex = request.form["sex"]
        purpose = request.form["purpose"]
        stretch_level = request.form["stretch_level"]
        activity_level = request.form["activity_level"]

        user.age = age
        user.height = height
        user.weight = weight
        user.sex = sex
        user.purpose = purpose
        user.stretch_level = stretch_level
        user.activity_level = activity_level
        db.session.commit()
        return redirect("/index")
    return render_template("profile.html", user=user)


@app.route("/display_log", methods=["GET"])
@login_required
def display_log():
    user_id = session.get("user_id")
    user = db.session.get(User, user_id)
    meal_logs = db.session.query(MealLog).filter_by(user_id=user_id).all()
    stretch_logs = db.session.query(StretchLog).filter_by(user_id=user_id).all()

    # 24時間以内の食事記録を取得
    recent_meal_logs = get_recent_logs(MealLog, hours=24, user_id=user_id)
    recent_nutrients = calc_total_nutrients(recent_meal_logs)

    recent_stretch_logs = get_recent_logs(StretchLog, hours=24, user_id=user_id)
    recent_burned_calories = sum(log.energy for log in recent_stretch_logs)

    # 24時間以内の筋トレ記録をメニューごとに回数合計で集計
    stretch_menu_counts = collections.defaultdict(int)
    for log in recent_stretch_logs:
        stretch_menu_counts[log.stretch] += (
            log.sets * log.reps if log.sets or log.reps else 0
        )
    print(f"--- Stretch menu counts in last 24 hours: {dict(stretch_menu_counts)} ---")

    return render_template(
        "display_log.html",
        user=user,
        meal_logs=meal_logs,
        stretch_logs=stretch_logs,
        recent_meal_logs=recent_meal_logs,
        recent_nutrients=recent_nutrients,
        recent_stretch_logs=recent_stretch_logs,
        recent_burned_calories=recent_burned_calories,
        stretch_menu_counts=stretch_menu_counts,
    )


@app.route("/add_meal", methods=["GET", "POST"])
@login_required
def add_meal():
    user_id = session.get("user_id")
    user = db.session.get(User, user_id)
    if request.method == "POST":
        meal = request.form["meal"]
        amount = request.form["amount"]

        amount, energy, protein, carbs, fat, vitamins, minerals = (
            calc_nutrient_from_table(meal, amount)
        )
        meal_log = MealLog(
            user_id=user_id,
            meal=meal,
            amount=amount,
            energy=energy,
            protein=protein,
            carbs=carbs,
            fat=fat,
            vitamins=vitamins,
            minerals=minerals,
        )
        db.session.add(meal_log)
        db.session.commit()
        print("--- MEAL LOG ADDED ---")
        return redirect("/display_log")
    meals = pd.read_csv("csv/newFoodData_fromGovernment.csv").to_dict(orient="records")
    return render_template("add_meal.html", user=user, meals=meals)


@app.route("/<int:meal_log_id>/delete_meal", methods=["GET"])
@login_required
def delete_meal(meal_log_id):
    meal_log = MealLog.query.get_or_404(meal_log_id)
    db.session.delete(meal_log)
    db.session.commit()
    print("--- MEAL LOG DELETED ---")
    return redirect("/display_log")


@app.route("/add_stretch", methods=["GET", "POST"])
@login_required
def add_stretch():
    user_id = session.get("user_id")
    user = db.session.get(User, user_id)
    if request.method == "POST":
        stretch = request.form["stretch"]
        sets = request.form["sets"]
        reps = request.form["reps"]
        setTime = request.form["setTime"]
        weight = user.weight if user.weight else 60

        energy = calc_burned_calories(stretch, sets, reps, setTime, weight)

        stretch_log = StretchLog(
            user_id=user_id,
            stretch=stretch,
            sets=sets,
            reps=reps,
            setTime=setTime,
            energy=energy,
        )
        db.session.add(stretch_log)
        db.session.commit()
        print("--- STRETCH LOG ADDED ---")
        return redirect("/display_log")
    stretches = pd.read_csv("csv/TrainingData_60kg.csv").to_dict(orient="records")
    return render_template("add_stretch.html", user=user, stretches=stretches)


@app.route("/<int:stretch_log_id>/delete_stretch", methods=["GET"])
@login_required
def delete_stretch(stretch_log_id):
    stretch_log = StretchLog.query.get_or_404(stretch_log_id)
    db.session.delete(stretch_log)
    db.session.commit()
    print("--- STRETCH LOG DELETED ---")
    return redirect("/display_log")


@app.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        user_id = session.get("user_id")

        post = Post(title=title, body=body, user_id=user_id)
        db.session.add(post)
        db.session.commit()
        return redirect("/index")
    return render_template("create.html")


@app.route("/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == "POST":
        post.title = request.form["title"]
        post.body = request.form["body"]
        db.session.commit()
        return redirect("/index")
    return render_template("update.html", post=post)


@app.route("/<int:post_id>/delete", methods=["GET"])
@login_required
def delete(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect("/index")


@app.route("/logout")
@login_required
def logout():
    session.pop("user_id", None)
    logout_user()
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)
