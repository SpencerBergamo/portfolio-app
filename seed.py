from models import db, User, stageTestimonial, pushTestimonial

def seed_db():
    db.drop_all()
    db.create_all()

    admin_user = User(username='admin', password='password')
    db.session.add(admin_user)
    db.session.commit()

if __name__ == "__main__":
    seed_db()