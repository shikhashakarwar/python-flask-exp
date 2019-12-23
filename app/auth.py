# import funtools
from werkzeug.security import check_password_hash, generate_password_hash
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from app.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        if not username:
            error = "User name is required"
        elif not password:
            error = "Password is required"
        elif db.execute(
            'select id from user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = "User {} already exist in our system".format(username)
    
        if error is None:
            db.execute("insert into user (username, password) VALUES(?, ?)", 
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for("auth.login"))
        flash(error)
    return render_template("auth/register.html")

@bp.route("/login", methods=("POST",))
def login():
    username = request.form["username"]
    password = request.form["password"]
    db = get_db()
    error = None
    user = db.execute(
        'select id from user WHERE username = ?', (username,)
    ).fetchone()

    if user is None:
        error = "Incorrect user Name"
    elif not check_password_hash(user["password"], password):
        error = "Incorrect password"
    
    if error is None:
        session.clear()
        session['user_id'] = user['id']
        return redirect(url_for("index"))

    flash(error)
    return render_template("<h1>Login page</h1>")

@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            "select * from user where id = ?", (user_id)
        ).fetchone()
