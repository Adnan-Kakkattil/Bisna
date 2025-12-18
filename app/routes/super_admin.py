from flask import render_template, url_for, flash, redirect, request, Blueprint, make_response
from flask_login import login_required, current_user
from app import db
from app.models import User, Role, College
from app.forms import CollegeForm
from app.decorators import role_required
from app.utils import log_activity

super_admin = Blueprint('super_admin', __name__)

@super_admin.route('/super_admin/dashboard')
@login_required
@role_required('Super Admin')
def dashboard():
    colleges = College.query.all()
    # Pending Admins
    pending_users = User.query.join(Role).filter(
        User.is_verified == False,
        Role.name == 'Admin',
        User.college_id != None
    ).all()
    
    verified_admins = User.query.join(Role).filter(
        User.is_verified == True,
        Role.name.in_(['Admin', 'Super Admin'])
    ).all()
    
    return render_template('super_admin/dashboard.html', 
                           colleges=colleges, 
                           pending_users=pending_users,
                           verified_admins=verified_admins)

@super_admin.route('/super_admin/college/add', methods=['GET', 'POST'])
@login_required
@role_required('Super Admin')
def add_college():
    form = CollegeForm()
    if form.validate_on_submit():
        college = College(name=form.name.data)
        db.session.add(college)
        db.session.commit()
        log_activity('Add College', f'Added college {college.name}')
        flash('College Added!', 'success')
        return redirect(url_for('super_admin.dashboard'))
    return render_template('super_admin/manage.html', form=form, title='Add College')

@super_admin.route('/super_admin/verify/<int:user_id>/<action>')
@login_required
@role_required('Super Admin')
def verify_user(user_id, action):
    user = User.query.get_or_404(user_id)
    if action == 'approve':
        user.is_verified = True
        log_activity('Verify Admin', f'Approved admin {user.username}')
        flash(f'User {user.username} approved.', 'success')
    elif action == 'reject':
        username = user.username
        log_activity('Verify Admin', f'Rejected/Deleted admin {username}')
        db.session.delete(user)
        flash(f'User {username} rejected/deleted.', 'danger')
    
    db.session.commit()
    return redirect(url_for('super_admin.dashboard'))

@super_admin.route('/super_admin/college/edit/<int:college_id>', methods=['GET', 'POST'])
@login_required
@role_required('Super Admin')
def edit_college(college_id):
    college = College.query.get_or_404(college_id)
    form = CollegeForm()
    if form.validate_on_submit():
        college.name = form.name.data
        db.session.commit()
        log_activity('Edit College', f'Updated college name to {college.name}')
        flash('College Updated!', 'success')
        return redirect(url_for('super_admin.dashboard'))
    elif request.method == 'GET':
        form.name.data = college.name
    return render_template('super_admin/manage.html', form=form, title='Edit College')

@super_admin.route('/super_admin/logs')
@login_required
@role_required('Super Admin')
def view_logs():
    # Filter logs for 'Admin' role users
    from app.models import ActivityLog
    logs = ActivityLog.query.join(User).join(Role).filter(Role.name == 'Admin').order_by(ActivityLog.timestamp.desc()).all()
    return render_template('super_admin/logs.html', logs=logs, title='Admin Activity Logs')

@super_admin.route('/super_admin/college/delete/<int:college_id>', methods=['POST'])
@login_required
@role_required('Super Admin')
def delete_college(college_id):
    college = College.query.get_or_404(college_id)
    db.session.delete(college)
    db.session.commit()
    log_activity('Delete College', f'Deleted college {college.name}')
    flash(f'College "{college.name}" deleted successfully.', 'success')
    return redirect(url_for('super_admin.dashboard'))
@super_admin.route('/super_admin/admin/delete/<int:user_id>', methods=['POST'])
@login_required
@role_required('Super Admin')
def delete_admin(user_id):
    user = User.query.get_or_404(user_id)
    if user.role.name != 'Admin':
        flash('Unauthorized transition.', 'danger')
        return redirect(url_for('super_admin.dashboard'))
    
    username = user.username
    db.session.delete(user)
    db.session.commit()
    log_activity('Delete Admin', f'Deleted admin {username}')
    flash(f'Admin {username} deleted.', 'success')
    return redirect(url_for('super_admin.dashboard'))

@super_admin.route('/super_admin/report/<int:user_id>')
@login_required
@role_required('Super Admin')
def user_report(user_id):
    import io
    import csv
    from app.models import ActivityLog
    
    user = User.query.get_or_404(user_id)
    # Super Admin can see reports of any Admin
    if user.role.name != 'Admin':
        flash('Unauthorized transition.', 'danger')
        return redirect(url_for('super_admin.dashboard'))
    
    logs = ActivityLog.query.filter_by(user_id=user.id).order_by(ActivityLog.timestamp.desc()).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Admin Activity Report'])
    writer.writerow(['Username', user.username])
    writer.writerow(['Email', user.email])
    writer.writerow(['College', user.college.name if user.college else 'N/A'])
    writer.writerow([])
    writer.writerow(['Timestamp', 'Action', 'Details'])
    
    for log in logs:
        writer.writerow([log.timestamp.strftime('%Y-%m-%d %H:%M:%S'), log.action, log.details or ''])
    
    output.seek(0)
    
    response = make_response(output.getvalue())
    response.headers['Content-Disposition'] = f'attachment; filename=activity_report_{user.username}.csv'
    response.headers['Content-Type'] = 'text/csv'
    
    log_activity('Generate Report', f'Generated activity report for admin {user.username}')
    return response

@super_admin.route('/super_admin/download_all_logs')
@login_required
@role_required('Super Admin')
def download_all_logs():
    import io
    import csv
    from app.models import ActivityLog
    
    logs = ActivityLog.query.join(User).join(Role).filter(Role.name == 'Admin').order_by(ActivityLog.timestamp.desc()).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Global Admin Activity Logs'])
    writer.writerow(['Generated At', datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')])
    writer.writerow([])
    writer.writerow(['Timestamp', 'User', 'Email', 'College', 'Action', 'Details'])
    
    for log in logs:
        writer.writerow([
            log.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            log.user.username,
            log.user.email,
            log.user.college.name if log.user.college else 'N/A',
            log.action,
            log.details or ''
        ])
    
    output.seek(0)
    response = make_response(output.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=admin_activity_logs.csv'
    response.headers['Content-Type'] = 'text/csv'
    
    log_activity('Download Bulk Logs', 'Super Admin downloaded all admin activity logs')
    return response
