from app import create_app, db
from app.models import Role, User, College
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Only create tables if they don't exist. db.drop_all() is removed for safety.
    db.create_all()
    
    # Seed Roles
    roles = ['Super Admin', 'Admin', 'Teacher', 'Senior Student', 'Student']
    for role_name in roles:
        if not Role.query.filter_by(name=role_name).first():
            role = Role(name=role_name)
            db.session.add(role)
    
    db.session.commit()
    print("Roles seeded.")

    # Seed College
    demo_college = College(name='Demo Engineering College')
    db.session.add(demo_college)
    db.session.commit()
    print("Demo College seeded.")

    # Create Super Admin
    super_admin_role = Role.query.filter_by(name='Super Admin').first()
    super_user = User(
        username='superadmin',
        email='superadmin@example.com',
        password_hash=generate_password_hash('admin123'),
        role=super_admin_role,
        is_verified=True
    )
    db.session.add(super_user)
    db.session.commit()
    print("Super Admin created (superadmin@example.com / admin123).")
    
    print("Database initialized successfully.")
