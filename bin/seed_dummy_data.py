from app import create_app, db
from app.models import Role, User, College, Course, Semester, Subject, Unit, Topic, Note
from werkzeug.security import generate_password_hash
from datetime import datetime

def seed_data():
    app = create_app()
    with app.app_context():
        print("Starting data seeding...")
        
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

        # Colleges to create
        college_names = [
            "Global Institute of Technology",
            "Metropolitan University",
            "Eastern Science Academy"
        ]
        
        colleges = []
        for name in college_names:
            college = College.query.filter_by(name=name).first()
            if not college:
                college = College(name=name)
                db.session.add(college)
                db.session.commit()
                print(f"Created College: {name}")
            colleges.append(college)

        # For each college, create users and content
        for idx, college in enumerate(colleges):
            base_slug = college.name.lower().replace(" ", "")[:5]
            
            # 1. Admin
            admin_email = f"admin@{base_slug}.edu"
            if not User.query.filter_by(email=admin_email).first():
                admin = User(
                    username=admin_email,
                    email=admin_email,
                    password_hash=generate_password_hash('password123'),
                    role=role_objs['Admin'],
                    college=college,
                    is_verified=True
                )
                db.session.add(admin)
                print(f"  Created Admin: {admin_email}")

            # 2. Teacher
            teacher_email = f"teacher@{base_slug}.edu"
            teacher = User.query.filter_by(email=teacher_email).first()
            if not teacher:
                teacher = User(
                    username=teacher_email,
                    email=teacher_email,
                    password_hash=generate_password_hash('password123'),
                    role=role_objs['Teacher'],
                    college=college,
                    is_verified=True
                )
                db.session.add(teacher)
                print(f"  Created Teacher: {teacher_email}")

            # 3. Student
            student_email = f"student@{base_slug}.edu"
            if not User.query.filter_by(email=student_email).first():
                student = User(
                    username=student_email,
                    email=student_email,
                    password_hash=generate_password_hash('password123'),
                    role=role_objs['Student'],
                    college=college,
                    register_number=f"REG{idx}{100}",
                    is_verified=True
                )
                db.session.add(student)
                print(f"  Created Student: {student_email}")

            db.session.commit()

            # 4. Content Structure (Course -> Semester -> Subject -> Unit -> Topic)
            course_name = f"Computer Science - {college.name}"
            course = Course.query.filter_by(name=course_name, college_id=college.id).first()
            if not course:
                course = Course(name=course_name, college_id=college.id)
                db.session.add(course)
                db.session.commit()
                
                sem = Semester(number=1, course=course)
                db.session.add(sem)
                db.session.commit()
                
                sub = Subject(name=f"Data Structures ({college.name})", semester=sem)
                db.session.add(sub)
                db.session.commit()
                
                unit = Unit(number=1, subject=sub)
                db.session.add(unit)
                db.session.commit()
                
                topic = Topic(name=f"Linked Lists - {college.name}", unit=unit)
                db.session.add(topic)
                db.session.commit()
                
                # 5. Dummy Materials (Notes)
                note1 = Note(
                    title="Introduction to Linked Lists",
                    filename="sample.pdf",
                    file_url="https://res.cloudinary.com/demo/image/upload/v1312461204/sample.pdf",
                    material_type="pdf",
                    uploader=teacher,
                    topic=topic,
                    college_id=college.id,
                    is_verified=True
                )
                note2 = Note(
                    title="Visualization of Linked Lists",
                    filename="video_link",
                    file_url="https://www.youtube.com/watch?v=njTh_NpJK6c",
                    material_type="url",
                    uploader=teacher,
                    topic=topic,
                    college_id=college.id,
                    is_verified=True
                )
                db.session.add(note1)
                db.session.add(note2)
                db.session.commit()
                print(f"  Seeded content for {college.name}")

        print("Seeding completed successfully.")

if __name__ == "__main__":
    seed_data()
