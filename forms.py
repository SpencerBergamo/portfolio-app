from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Regexp

class AdminSignup(FlaskForm):    
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class UserLoginForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class AddTestimonialForm(FlaskForm):
    
    name = StringField('Name', validators=[DataRequired()])
    testimonial = TextAreaField('Testimonial', validators=[DataRequired()])
    rating = IntegerField('Rating', validators=[NumberRange(min=1, max=5)])


class QuoteForm(FlaskForm):

    name = StringField('Name', validators=[DataRequired()])
    organization = StringField('Organization', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    hosting = StringField('Hosting', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])