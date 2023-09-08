from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username =  db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)

    @classmethod
    def signup(cls, username, password):
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')
        user = User(username=username, password=hashed_pwd)
        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else: 
            return False 

class stageTestimonial(db.Model):
    __tablename__ = 'stage_testimonial'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    testimonial = db.Column(db.String(1000), nullable=False)
    rating = db.Column(db.Integer, nullable=False)


class pushTestimonial(db.Model):
    __tablename__ = 'push_testimonial'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    testimonial = db.Column(db.String(1000), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

def connect_db(app):
    db.app = app
    db.init_app(app)

