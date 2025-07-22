from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify
from flask_login import login_required, current_user
import requests
from forms.user_forms import UserProfileForm

bp = Blueprint('users', __name__, url_prefix='/users')

@bp.route('/')
@login_required
def index():
    try:
        # Fetch all users belonging to the current matchmaker
        headers = {'Authorization': f'Bearer {current_user.token}'}
        response = requests.get(
            f"{current_app.config['API_URL']}/matchmaker/users",
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            print(data)
            # Extract users from the nested structure
            users = data.get('users', [])
            return render_template('users/index.html', users=users)
        else:
            print(response.json())
            flash('Failed to retrieve users.', 'danger')
            return render_template('users/index.html', users=[])
    except Exception as e:
        flash(f"Connection error: {str(e)}", 'danger')
        return render_template('users/index.html', users=[])

@bp.route('/new', methods=['GET', 'POST'])
@login_required
def create():
    form = UserProfileForm()
    if form.validate_on_submit():
        try:
            # Create user profile via API
            headers = {'Authorization': f'Bearer {current_user.token}'}
            user_data = form.data.copy()
            # Remove CSRF token and submit button from form data
            user_data.pop('csrf_token', None)
            user_data.pop('submit', None)
            
            response = requests.post(
                f"{current_app.config['API_URL']}/user",
                json=user_data,
                headers=headers
            )
            
            if response.status_code == 201:
                flash('User profile created successfully!', 'success')
                return redirect(url_for('users.index'))
            else:
                error_msg = response.json().get('message', 'Failed to create user profile')
                flash(error_msg, 'danger')
        except Exception as e:
            flash(f"Connection error: {str(e)}", 'danger')
    
    return render_template('users/create.html', form=form)

@bp.route('/<int:user_id>', methods=['GET'])
@login_required
def view(user_id):
    try:
        # Fetch user details via API
        headers = {'Authorization': f'Bearer {current_user.token}'}
        response = requests.get(
            f"{current_app.config['API_URL']}/user/{user_id}",
            headers=headers
        )
        
        if response.status_code == 200:
            user = response.json()
            return render_template('users/view.html', user=user)
        else:
            flash('User not found or access denied.', 'danger')
            return redirect(url_for('users.index'))
    except Exception as e:
        flash(f"Connection error: {str(e)}", 'danger')
        return redirect(url_for('users.index'))

@bp.route('/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(user_id):
    try:
        # Fetch user details for editing
        headers = {'Authorization': f'Bearer {current_user.token}'}
        response = requests.get(
            f"{current_app.config['API_URL']}/user/{user_id}",
            headers=headers
        )
        
        if response.status_code != 200:
            flash('User not found or access denied.', 'danger')
            return redirect(url_for('users.index'))
        
        user_data = response.json()
        form = UserProfileForm(obj=user_data)
        
        if form.validate_on_submit():
            # Update user profile via API
            update_data = form.data.copy()
            # Remove CSRF token and submit button from form data
            update_data.pop('csrf_token', None)
            update_data.pop('submit', None)
            
            update_response = requests.put(
                f"{current_app.config['API_URL']}/user/{user_id}",
                json=update_data,
                headers=headers
            )
            
            if update_response.status_code == 200:
                flash('User profile updated successfully!', 'success')
                return redirect(url_for('users.view', user_id=user_id))
            else:
                error_msg = update_response.json().get('message', 'Failed to update user profile')
                flash(error_msg, 'danger')
        
        return render_template('users/edit.html', form=form, user_id=user_id)
    except Exception as e:
        flash(f"Connection error: {str(e)}", 'danger')
        return redirect(url_for('users.index')) 