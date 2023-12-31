import os
from flask import Flask, render_template, request, flash, redirect, session, g, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from forms import AdminSignup, UserLoginForm, AddTestimonialForm, QuoteForm
from models import db, connect_db, User, stageTestimonial, pushTestimonial
from flask_mail import Mail, Message
import requests

# python3 -m venv venv
# source venv/bin/activate
# pip3 install -r dependencies.txt
# python3 -m app.py

CURR_USER_KEY = "curr_user"

app = Flask(__name__, static_url_path='/static', static_folder='static')
port = int(os.environ.get("PORT", 5000))

def get_database_url() -> str:
    """Get database URL from environment variable or config file."""
    try:
        return os.environ["DATABASE_URL"].replace("://", "ql://", 1)
    except AttributeError:
        print("No environment variable 'DATABASE_URL' found. Using config file.")
    return "postgres:///sihgxuqzqokubx:46792bd6c3fddba482b51ac9eea5c4a380df8c53bcdb87b842adbe7fa3780dce@ec2-3-218-172-130.compute-1.amazonaws.com:5432/d18lumgvm46oje"


SLACK_WEBHOOK = ''
app.config['SQLALCHEMY_DATABASE_URI'] = get_database_url()
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql:///portfolio')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'myportfolio')
toolbar = DebugToolbarExtension(app)

connect_db(app)

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None

def do_login(user):
    """Log in user."""
    session[CURR_USER_KEY] = user.id

def do_logout():
    """Logout user."""
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

# User first route
@app.route('/')
def root():
    return redirect('/homepage')

@app.route('/homepage')
def homepage():
    push_testimonials = pushTestimonial.query.all()
    return render_template('/homepage.html', push_testimonials=push_testimonials)

@app.route('/admin-signup', methods=['GET', 'POST'])
def admin_signup():
    form = AdminSignup()
    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data, 
                password=form.password.data)
            db.session.commit()
        except IntegrityError:
            # flash("Username already taken", 'danger')
            return render_template('adminsignup.html', form=form)
        do_login(user)
        # flash(f"Hello, {user.username}!", "success")
        return redirect('/stage-testimonials')
    return render_template('signup.html', form=form)

@app.route('/admin-signin', methods=['GET', 'POST'])
def admin_signin():
    form = UserLoginForm()
    if form.validate_on_submit():
        user = User.authenticate(
            username=form.username.data, 
            password=form.password.data)
        if user:
            do_login(user)
            # flash(f"Hello, {user.username}!", "success")
            return redirect('/stage-testimonials')
        # flash("Invalid credentials.", 'danger')
    return render_template('adminlogin.html', form=form)

@app.route('/logout') 
def logout():
    do_logout()
    return redirect('/homepage')

# Testimonials
@app.route('/add_testimonial', methods=['GET', 'POST'])
def add_testimonial():
    form = AddTestimonialForm()
    if form.validate_on_submit():
        new_testimonial = stageTestimonial(
            name=form.name.data, 
            testimonial=form.testimonial.data, 
            rating=form.rating.data)
        db.session.add(new_testimonial)
        db.session.commit()
        flash("Testimonial added successfully, your review is under review 😜", "success")
        return redirect('/homepage')
    return render_template('/addtestimonial.html', form=form)

# Stage and Push Testimonials
@app.route('/stage-testimonials')
def stage_testimonials():
    stage_testimonials = stageTestimonial.query.all()
    push_testimonials = pushTestimonial.query.all()

    return render_template('/testimonials.html', stage_testimonials=stage_testimonials, push_testimonials=push_testimonials)

@app.route('/push-testimonials/<int:testimonial_id>', methods=['POST'])
def push_testimonials(testimonial_id):
    testimonial = stageTestimonial.query.get_or_404(testimonial_id)

    new_pushed_testimonial = pushTestimonial(
        name=testimonial.name,
        testimonial=testimonial.testimonial,
        rating=testimonial.rating
    )
    db.session.add(new_pushed_testimonial)
    db.session.delete(testimonial)
    db.session.commit()
    return redirect('/stage-testimonials')

@app.route('/delete-stage-id/<int:testimonial_id>', methods=['POST'])
def delete_stage_id(testimonial_id):
    testimonial = stageTestimonial.query.get_or_404(testimonial_id)
    db.session.delete(testimonial)
    db.session.commit()
    return redirect('/stage-testimonials')

@app.route('/delete-push-id/<int:testimonial_id>', methods=['POST'])
def delete_push_id(testimonial_id):
    testimonial = pushTestimonial.query.get_or_404(testimonial_id)
    db.session.delete(testimonial)
    db.session.commit()
    return redirect('/stage-testimonials')

@app.route('/quote-form', methods=['GET', 'POST'])
def quote_form():
    form = QuoteForm()

    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        organization = form.organization.data
        email = form.email.data
        phone = form.phone.data
        hosting = form.hosting.data
        description = form.description.data

        slack_message = f"New Quote:\nName: {name}\nOrganization: {organization}\nEmail: {email}\nPhone: {phone}\nHosting: {hosting}\nDescription: {description}"

        quote_send(slack_message)

        flash("Your quote has been sent, I will get back to you soon!", "success")

        return redirect('/homepage')
    
    return render_template('/quote.html', form=form)

@app.route('/quote-send', methods=['POST'])
def quote_send(message):
    try:
        response = requests.post(
            SLACK_WEBHOOK,
            json={'text': message}       
        )
        if response.status_code == 200:

            return jsonify(success=True, message="Message sent")
        else:
            return jsonify(success=False, message="Message failed")
        
    except Exception as e:
        print(f"Error sending slack message: {e}")
        return jsonify(success=False, message="Message failed")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=False, port=port)