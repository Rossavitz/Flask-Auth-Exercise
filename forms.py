from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import InputRequired, Email, Length


class UserForm(FlaskForm):
    """user info form"""

    username = StringField(
        "Username",
        validators=[
            InputRequired(),
            Length(min=1, max=20),
        ],
    )
    password = PasswordField(
        "Password", validators=[InputRequired(), Length(min=6, max=15)]
    )
    email = EmailField("Email", validators=[InputRequired(), Email()])

    first_name = StringField(
        "First Name",
        validators=[
            InputRequired(),
            Length(max=30),
        ],
    )

    last_name = StringField(
        "Last Name",
        validators=[
            InputRequired(),
            Length(max=30),
        ],
    )


class LoginForm(FlaskForm):
    """login form"""

    username = StringField(
        "Username",
        validators=[
            InputRequired(),
            Length(min=1, max=20),
        ],
    )
    password = PasswordField(
        "Password", validators=[InputRequired(), Length(min=6, max=15)]
    )


class FeedbackForm(FlaskForm):
    """feedback form"""

    title = StringField(
        "Title",
        validators=[InputRequired(), Length(max=50)],
    )

    content = StringField("Content", validators=[InputRequired()])
