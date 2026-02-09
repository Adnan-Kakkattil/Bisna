import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import Role, User, College, Course, Semester, Subject, Unit, Topic, Note, VerificationStatus
from werkzeug.security import generate_password_hash
from datetime import datetime
import random

def seed_final_data():
    app = create_app()
    with app.app_context():
        print("🚀 Starting final data seeding...")
        
        # 1. Ensure Roles exist
        roles_list = ['Super Admin', 'Admin', 'Teacher', 'Senior Student', 'Student']
        role_objs = {}
        for r_name in roles_list:
            role = Role.query.filter_by(name=r_name).first()
            if not role:
                role = Role(name=r_name)
                db.session.add(role)
                db.session.commit()
            role_objs[r_name] = role

        # 2. Ensure Super Admin exists
        super_admin_email = "superadmin@example.com"
        if not User.query.filter_by(email=super_admin_email).first():
            super_admin = User(
                username="super_admin",
                email=super_admin_email,
                password_hash=generate_password_hash("admin123"),
                role=role_objs['Super Admin'],
                is_verified=True
            )
            db.session.add(super_admin)
            db.session.commit()
            print(f"✅ Created Super Admin: {super_admin_email}")

        # 3. Colleges
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
                print(f"🏫 Created College: {c_name} (ID: {college.formatted_id})")
            
            base_slug = c_name.lower().replace(" ", "")[:5]
            
            # 4. Content Structure per College (Need a basic syllabus for notes)
            course_name = f"Computer Science - {college.name}"
            course = Course.query.filter_by(name=course_name, college_id=college.id).first()
            if not course:
                course = Course(name=course_name, college_id=college.id)
                db.session.add(course)
                db.session.commit()
                sem = Semester(number=1, course=course)
                db.session.add(sem)
                db.session.commit()
                sub = Subject(name=f"Systems Architecture", semester=sem)
                db.session.add(sub)
                db.session.commit()
                unit = Unit(number=1, subject=sub)
                db.session.add(unit)
                db.session.commit()
                topic = Topic(name=f"Kernel Structures", unit=unit)
                db.session.add(topic)
                db.session.commit()
            else:
                topic = Topic.query.join(Unit).join(Subject).join(Semester).filter(Semester.course_id == course.id).first()

            # 5. Admin (1 per college)
            admin_email = f"admin@{base_slug}.edu"
            if not User.query.filter_by(email=admin_email).first():
                admin = User(
                    username=f"admin_{base_slug}",
                    email=admin_email,
                    password_hash=default_password,
                    role=role_objs['Admin'],
                    college_id=college.id,
                    is_verified=True
                )
                db.session.add(admin)

            # 6. Teachers (10 per college)
            teacher_names = [
                "Dr. Alan Turing", "Prof. Grace Hopper", "Dr. John von Neumann", 
                "Prof. Ada Lovelace", "Dr. Claude Shannon", "Prof. Barbara Liskov",
                "Dr. Tim Berners-Lee", "Prof. Donald Knuth", "Dr. Ken Thompson", "Prof. Linus Torvalds"
            ]
            for t_idx in range(1, 11):
                teacher_email = f"teacher{t_idx}@{base_slug}.edu"
                teacher_name = teacher_names[t_idx-1]
                teacher = User.query.filter_by(email=teacher_email).first()
                if not teacher:
                    teacher = User(
                        username=f"teacher{t_idx}_{base_slug}",
                        name=teacher_name,
                        email=teacher_email,
                        password_hash=default_password,
                        role=role_objs['Teacher'],
                        college_id=college.id,
                        is_verified=True
                    )
                    db.session.add(teacher)
                    db.session.commit() # Commit to get teacher ID for student/note creation

                # 7. Students (10 per teacher = 100 per college)
                for s_idx in range(1, 11):
                    student_email = f"student{t_idx}_{s_idx}@{base_slug}.edu"
                    if not User.query.filter_by(email=student_email).first():
                        student = User(
                            username=f"student{t_idx}_{s_idx}_{base_slug}",
                            name=f"Student {t_idx}-{s_idx}",
                            email=student_email,
                            password_hash=default_password,
                            role=role_objs['Student'],
                            college_id=college.id,
                            register_number=f"REG{c_idx+1}{t_idx:02d}{s_idx:02d}",
                            is_verified=True
                        )
                        db.session.add(student)

                # 8. Resources (3 per teacher)
                # Check if this teacher already has notes
                if Note.query.filter_by(user_id=teacher.id).count() < 3:
                    resource_types = [
                        ("Lecture Notes - Unit 1", "sample_notes.pdf", "pdf"),
                        ("Course Syllabus Overview", "syllabus.docx", "docx"),
                        ("Architecture Diagram", "https://res.cloudinary.com/demo/image/upload/sample.jpg", "url")
                    ]
                    for r_title, r_file, r_type in resource_types:
                        note = Note(
                            title=f"{r_title} ({teacher.name})",
                            filename=r_file if r_type != "url" else "External Link",
                            file_url=r_file if r_type == "url" else "https://res.cloudinary.com/demo/image/upload/v1312461204/sample.pdf",
                            material_type=r_type,
                            uploader=teacher,
                            topic=topic,
                            college_id=college.id,
                            is_verified=True
                        )
                        db.session.add(note)
                        db.session.commit()
                        
                        # Add verification status record
                        v_status = VerificationStatus(
                            note_id=note.id,
                            verifier_id=teacher.id, # Self-verified for dummy data
                            status='Approved',
                            comments='System seeded data.',
                            verified_at=datetime.utcnow()
                        )
                        db.session.add(v_status)

            db.session.commit()
            print(f"  ✨ Seeded {c_name}: 1 Admin, 10 Teachers, 100 Students, 30 Resources.")

        print("🎉 Final seeding completed successfully!")

if __name__ == "__main__":
    seed_final_data()
