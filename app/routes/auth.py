from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from app import db
from app.models import User, Role, College, StudentRegistry
from app.forms import RegistrationForm, LoginForm, AdminRegistrationForm, SuperAdminRegistrationForm
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    form.college.choices = [(c.id, c.name) for c in College.query.all()]
    
    if form.validate_on_submit():
        role = Role.query.filter_by(name=form.role.data).first()
        if not role:
            flash('Error: Roles not initialized.', 'danger')
            return redirect(url_for('auth.register'))
            
        hashed_password = generate_password_hash(form.password.data)
        
        # Determine College ID based on role
        from app.utils import parse_college_id
        if role.name == 'Admin':
            college_id = form.college.data
        else:
            college_id = parse_college_id(form.college_id.data)
            if college_id is None:
                flash('Invalid College ID Format. Use CIDAxxx.', 'danger')
                return render_template('auth/register.html', title='Register', form=form)

        college = College.query.get(college_id)
        if not college:
            flash('Invalid College selection or ID provided.', 'danger')
            return render_template('auth/register.html', title='Register', form=form)

        # Student specific logic
        if role.name == 'Student':
            email = form.email.data
            reg_num = form.register_number.data
            # Check registry based on BOTH Email and Register Number
            registry_entry = StudentRegistry.query.filter_by(
                email=email, 
                register_number=reg_num, 
                college_id=college_id
            ).first()
            
            if not registry_entry:
                flash('Registration failed: Email or Register Number not found in the College Registry.', 'danger')
                return render_template('auth/register.html', title='Register', form=form)
                
            if registry_entry.is_registered:
                flash('This student is already registered.', 'warning')
                return render_template('auth/register.html', title='Register', form=form)

            # Valid student - Create user
            # We save register_number if they typed it, but verification was pure email
            user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password, role=role,
                        college_id=college_id, register_number=reg_num, is_verified=True)
            
            registry_entry.is_registered = True
            db.session.add(user)
            db.session.commit()
            flash('Account created! You are verified and can log in.', 'success')
            return redirect(url_for('auth.login'))

        # Teacher logic
        elif role.name == 'Teacher':
             # College ID validation already done above
             user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password, role=role,
                        college_id=college_id, is_verified=False)
             db.session.add(user)
             db.session.commit()
             flash('Account created! Please wait for Admin/Principal verification.', 'info')
             return redirect(url_for('auth.login'))

        # Admin logic
        elif role.name == 'Admin':
             user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password, role=role,
                        college_id=college_id, is_verified=False)
             db.session.add(user)
             db.session.commit()
             flash('Admin Account created! Please wait for Super Admin verification.', 'info')
             return redirect(url_for('auth.login'))
            
    return render_template('auth/register.html', title='Register', form=form)

@auth.route("/register/admin", methods=['GET', 'POST'])
def register_admin():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = AdminRegistrationForm()
    form.college.choices = [(c.id, c.name) for c in College.query.all()]
    
    if form.validate_on_submit():
        role = Role.query.filter_by(name='Admin').first()
        hashed_password = generate_password_hash(form.password.data)
        
        user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password, role=role,
                    college_id=form.college.data, is_verified=False)
        db.session.add(user)
        db.session.commit()
        flash('Admin Account created! Please wait for Super Admin verification.', 'info')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/register_admin.html', title='Register Admin', form=form)

@auth.route("/register/super-admin", methods=['GET', 'POST'])
def register_super_admin():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = SuperAdminRegistrationForm()
    
    if form.validate_on_submit():
        role = Role.query.filter_by(name='Super Admin').first()
        hashed_password = generate_password_hash(form.password.data)
        
        # Super Admin is inherently verified and college-less
        user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password, role=role,
                    college_id=None, is_verified=True)
        db.session.add(user)
        db.session.commit()
        flash('Super Admin Account created successfully!', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/register_super_admin.html', title='Register Super Admin', form=form)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and check_password_hash(user.password_hash, form.password.data):
             # Verify Role Match
            if user.role.name != form.role.data:
                 # Map 'Admin' choice to 'Admin' role etc.
                 # The choices are: Student, Teacher, Admin, Super Admin.
                 # The Role names are: Student, Teacher, Admin, Super Admin.
                 # Perfect match expected.
                 flash(f'Role mismatch. You are registered as a {user.role.name}, not {form.role.data}.', 'danger')
                 return render_template('auth/login.html', title='Login', form=form)

             # Check College ID Match (skip for Super Admin)
            if user.role.name != 'Super Admin':
                if not form.college_id.data:
                     flash('College ID is required for this user.', 'danger')
                     return render_template('auth/login.html', title='Login', form=form)
                
                # Parse Input
                from app.utils import parse_college_id
                input_college_id = parse_college_id(form.college_id.data)

                if input_college_id is None:
                     flash('Invalid College ID Format.', 'danger')
                     return render_template('auth/login.html', title='Login', form=form)

                if user.college_id != input_college_id:
                     flash('Invalid College ID provided for this user.', 'danger')
                     return render_template('auth/login.html', title='Login', form=form)

            # Verification check
            # Skip for Super Admin (assuming they are always verified/handling self)
            if user.role.name != 'Super Admin' and not user.is_verified:
                 flash('Login Unsuccessful. Your account is pending verification.', 'warning')
                 return render_template('auth/login.html', title='Login', form=form)

            login_user(user, remember=form.remember.data)
            
            # Log Activity
            from app.utils import log_activity
            log_activity('Login', f'User {user.username} logged in.')
            
            next_page = request.args.get('next')
            
            # Redirect Super Admin to their dashboard
            if user.role.name == 'Super Admin':
                return redirect(url_for('super_admin.dashboard'))

            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('auth/login.html', title='Login', form=form)

@auth.route("/logout")
def logout():
    if current_user.is_authenticated:
        from app.utils import log_activity
        log_activity('Logout', f'User {current_user.username} logged out.')
    logout_user()
    return redirect(url_for('main.index'))

@auth.route("/profile")
@login_required
def profile():
    return render_template('auth/profile.html', title='User Profile')
