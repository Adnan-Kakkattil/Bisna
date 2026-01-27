from app import create_app, db
from app.models import User, College, StudentRegistry, Course, Semester, Subject, Unit, Topic, Note, VerificationStatus, ActivityLog

def clear_all_college_data():
    app = create_app()
    with app.app_context():
        print("Starting data cleanup...")
        
        try:
            # 1. Delete Activity Logs
            num_logs = ActivityLog.query.delete()
            print(f"Deleted {num_logs} ActivityLogs.")
            
            # 2. Delete Verification Statuses
            num_verifications = VerificationStatus.query.delete()
            print(f"Deleted {num_verifications} VerificationStatuses.")
            
            # 3. Delete Notes
            num_notes = Note.query.delete()
            print(f"Deleted {num_notes} Notes.")
            
            # 4. Delete Syllabus structure (Topics -> Units -> Subjects -> Semesters -> Courses)
            # Cascade delete should technically handle this if set up, but let's be explicit or safe
            num_topics = Topic.query.delete()
            num_units = Unit.query.delete()
            num_subjects = Subject.query.delete()
            num_semesters = Semester.query.delete()
            num_courses = Course.query.delete()
            print(f"Deleted Syllabus items: {num_courses} Courses, {num_semesters} Semesters, {num_subjects} Subjects, {num_units} Units, {num_topics} Topics.")
            
            # 5. Delete Student Registry
            num_registry = StudentRegistry.query.delete()
            print(f"Deleted {num_registry} StudentRegistry entries.")
            
            # 6. Delete Users (Except Super Admin)
            # Find users who are NOT Super Admin
            users_to_delete = User.query.filter(User.role_id != 1).all() # Assuming Role ID 1 is Super Admin based on setup_db.py
            # Safer way: check role name
            from app.models import Role
            super_admin_role = Role.query.filter_by(name='Super Admin').first()
            if super_admin_role:
                non_super_admins = User.query.filter(User.role_id != super_admin_role.id).all()
                num_users = len(non_super_admins)
                for u in non_super_admins:
                    db.session.delete(u)
                print(f"Deleted {num_users} non-Super Admin users.")
            
            # 7. Delete Colleges
            num_colleges = College.query.delete()
            print(f"Deleted {num_colleges} Colleges.")
            
            db.session.commit()
            print("Cleanup completed successfully.")
            
        except Exception as e:
            db.session.rollback()
            print(f"Cleanup failed: {e}")

if __name__ == "__main__":
    clear_all_college_data()
