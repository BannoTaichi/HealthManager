from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.String(300), nullable=False)
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now(pytz.timezone("Asia/Tokyo"))
    )


@app.route("/")
def index():
    if request.method == "GET":
        posts = Post.query.all()
        return render_template("index.html", posts=posts)


@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]

        post = Post(title=title, body=body)
        db.session.add(post)
        db.session.commit()
        return redirect("/")
    return render_template("create.html")


@app.route("/<int:post_id>/update", methods=["GET", "POST"])
def update(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == "POST":
        post.title = request.form["title"]
        post.body = request.form["body"]
        db.session.commit()
        return redirect("/")
    return render_template("update.html", post=post)


@app.route("/<int:post_id>/delete", methods=["GET"])
def delete(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
