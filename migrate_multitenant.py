from app import create_app, db
from sqlalchemy import text

app = create_app()
with app.app_context():
    try:
        # Course table
        db.session.execute(text("ALTER TABLE course ADD COLUMN college_id INTEGER REFERENCES college(id) DEFAULT 1;"))
        # Note table
        db.session.execute(text("ALTER TABLE note ADD COLUMN college_id INTEGER REFERENCES college(id) DEFAULT 1;"))
        
        db.session.commit()
        print("Successfully migrated course and note tables.")
    except Exception as e:
        print(f"Migration error: {e}")
