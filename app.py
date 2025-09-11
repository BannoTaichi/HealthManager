from flask import Flask, render_template, request, redirect, session, url_for
import os
from flask_login import LoginManager, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from database import db, User, Post, MealLog, StretchLog
from model import calc_nutrient

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
app.config["SECRET_KEY"] = os.urandom(24)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


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
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            login_user(user)
            return redirect("/index")
    return render_template("login.html")


@app.route("/index", methods=["GET"])
@login_required
def index():
    user_id = session.get("user_id")
    user = User.query.get(user_id)
    posts = Post.query.filter_by(user_id=user_id).all()
    return render_template("index.html", posts=posts, user=user)


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    user_id = session.get("user_id")
    user = User.query.get(user_id)
    if request.method == "POST":
        age = request.form["age"]
        height = request.form["height"]
        weight = request.form["weight"]
        activity_level = request.form["activity_level"]
        user.age = age
        user.height = height
        user.weight = weight
        user.activity_level = activity_level
        db.session.commit()
        return redirect("/index")
    return render_template("profile.html", user=user)


@app.route("/display_log", methods=["GET"])
@login_required
def display_log():
    user_id = session.get("user_id")
    user = User.query.get(user_id)
    meal_logs = MealLog.query.filter_by(user_id=user_id).all()
    stretch_logs = StretchLog.query.filter_by(user_id=user_id).all()
    return render_template(
        "display_log.html", user=user, meal_logs=meal_logs, stretch_logs=stretch_logs
    )


@app.route("/add_meal", methods=["GET", "POST"])
@login_required
def add_meal():
    user_id = session.get("user_id")
    user = User.query.get(user_id)
    if request.method == "POST":
        meal = request.form["meal"]
        amount = request.form["amount"]

        amount, energy, protein, carbs, fat, vitamins, minerals = calc_nutrient(
            meal, amount
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
        return redirect("/display_log")
    return render_template("add_meal.html", user=user)


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
