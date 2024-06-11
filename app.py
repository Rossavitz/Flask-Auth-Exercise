from flask import Flask, redirect, session, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, User, db, Feedback
from forms import UserForm, LoginForm, FeedbackForm
from werkzeug.exceptions import Unauthorized

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///auth_exercise"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

toolbar = DebugToolbarExtension(app)

app.app_context().push()
connect_db(app)


@app.route("/")
def home_page():
    """home page redirects to registration"""
    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def register_user():
    """Form to register a new user, also to handle form submit"""

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username, password, email, first_name, last_name)

        db.session.commit()
        session["username"] = user.username
        flash("User Added")
        return redirect("/login")
    else:
        return render_template("register.html", form=form)


@app.route("/users/<username>")
def get_user_info(username):
    """show info on a single user"""
    if "username" not in session or username != session["username"]:
        raise Unauthorized()

    user = User.query.get(username)
    return render_template("userinfo.html", user=user)


@app.route("/login", methods=["GET", "POST"])
def login_user():
    """Form to log in a user, also to handle that form"""

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            session["username"] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ["Invalid username/password."]
            return render_template("login.html", form=form)
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    """logout user"""
    session.pop("username")
    return redirect("/")


@app.route("/users/<username>/delete", methods=["GET"])
def delete_user(username):
    """Remove a user"""
    if "username" not in session or username != session["username"]:
        raise Unauthorized()

    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")
    # flash("User deleted!")
    return redirect("/login")


@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def create_feedback(username):
    """show feedback form and handle submission"""

    if "username" not in session or username != session["username"]:
        raise Unauthorized()

    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(
            title=title,
            content=content,
            username=username,
        )

        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    else:
        return render_template("/feedback.html", form=form)


@app.route("/feedback/<feedback_id>/update", methods=["GET", "POST"])
def update_feedback(feedback_id):
    """display form to edit feedback and handle submission"""

    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session["username"]:
        raise Unauthorized()

    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    else:
        return render_template("feedbackEdit.html", form=form, feedback=feedback)


@app.route("/feedback/<feedback_id>/delete", methods=["GET"])
def delete_feedback(feedback_id):
    """delete feedback"""

    feedback = Feedback.query.get(feedback_id)

    db.session.delete(feedback)
    db.session.commit()

    return redirect(f"/users/{feedback.username}")
