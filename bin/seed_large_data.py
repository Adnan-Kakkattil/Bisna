from app import create_app, db
from app.models import Role, User, College, Course, Semester, Subject, Unit, Topic, Note
from werkzeug.security import generate_password_hash
import random

def seed_large_data():
    app = create_app()
    with app.app_context():
        print("Starting large scale data seeding...")
        
        # Ensure Roles exist
        roles_list = ['Super Admin', 'Admin', 'Teacher', 'Senior Student', 'Student']
        role_objs = {}
        for r_name in roles_list:
            role = Role.query.filter_by(name=r_name).first()
            if not role:
                role = Role(name=r_name)
                db.session.add(role)
                db.session.commit()
            role_objs[r_name] = role

        college_names = [
            "Oxford Technical University",
            "Cambridge Science Academy",
            "Stanford Institute of Excellence",
            "MIT Global College",
            "Ethoz Business School",
            "Apex Engineering Institute"
        ]
        
        default_password = generate_password_hash('password123')

        for c_idx, c_name in enumerate(college_names):
            college = College.query.filter_by(name=c_name).first()
            if not college:
                college = College(name=c_name)
                db.session.add(college)
                db.session.commit()
                print(f"Created College: {c_name}")
            
            base_slug = c_name.lower().replace(" ", "")[:5]
            
            # 1. Admin
            admin_email = f"admin@{base_slug}.edu"
            if not User.query.filter_by(email=admin_email).first():
                admin = User(
                    username=admin_email,
                    email=admin_email,
                    password_hash=default_password,
                    role=role_objs['Admin'],
                    college_id=college.id,
                    is_verified=True
                )
                db.session.add(admin)

            # 2. Teachers (10 per college)
            for t_idx in range(1, 11):
                teacher_email = f"teacher{t_idx}@{base_slug}.edu"
                teacher = User.query.filter_by(email=teacher_email).first()
                if not teacher:
                    teacher = User(
                        username=teacher_email,
                        email=teacher_email,
                        password_hash=default_password,
                        role=role_objs['Teacher'],
                        college_id=college.id,
                        is_verified=True
                    )
                    db.session.add(teacher)
                    db.session.commit() # Commit to get teacher ID for student creation

                # 3. Students (10 per teacher)
                for s_idx in range(1, 11):
                    student_email = f"student{t_idx}_{s_idx}@{base_slug}.edu"
                    if not User.query.filter_by(email=student_email).first():
                        student = User(
                            username=student_email,
                            email=student_email,
                            password_hash=default_password,
                            role=role_objs['Student'],
                            college_id=college.id,
                            register_number=f"REG{c_idx+1}{t_idx:02d}{s_idx:02d}",
                            is_verified=True
                        )
                        db.session.add(student)
            
            db.session.commit()
            print(f"  Finished seeding {c_name} (1 Admin, 10 Teachers, 100 Students)")

        print("Large scale seeding completed successfully.")

if __name__ == "__main__":
    seed_large_data()
