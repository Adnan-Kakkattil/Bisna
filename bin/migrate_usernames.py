from app import create_app, db
from app.models import User

def migrate():
    app = create_app()
    with app.app_context():
        print("Starting username migration...")
        users = User.query.all()
        for user in users:
            if user.username != user.email:
                print(f"Updating {user.username} -> {user.email}")
                user.username = user.email
        
        try:
            db.session.commit()
            print("Migration successful.")
        except Exception as e:
            db.session.rollback()
            print(f"Migration failed: {e}")

if __name__ == "__main__":
    migrate()
