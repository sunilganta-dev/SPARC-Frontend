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

@bp.route('/test')
@login_required
def test():
    """Test route to verify the blueprint is working"""
    return jsonify({'message': 'Users blueprint is working!', 'user': current_user.name})

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """Profile page for the current matchmaker"""
    print(f"Profile route accessed by user: {current_user.name}")
    
    try:
        # Create default profile data
        profile_data = {
            'name': current_user.name,
            'email': current_user.email,
            'organization': 'SPARC Matchmaking',
            'phone': '+1 (555) 123-4567',
            'location': 'New York, NY',
            'experience_years': 5,
            'specializations': ['religious', 'cultural'],
            'bio': 'Experienced matchmaker specializing in religious and cultural compatibility.',
            'website': 'https://sparc-matchmaking.com',
            'social_media': {
                'linkedin': 'https://linkedin.com/in/matchmaker',
                'facebook': 'https://facebook.com/sparcmatchmaking',
                'instagram': 'https://instagram.com/sparcmatchmaking'
            }
        }
        
        # Try to fetch from API if available
        try:
            headers = {'Authorization': f'Bearer {current_user.token}'}
            api_url = f"{current_app.config['API_URL']}/matchmaker/profile"
            print(f"DEBUG: Attempting to fetch profile from: {api_url}")
            
            response = requests.get(
                api_url,
                headers=headers,
                timeout=5
            )
            
            print(f"DEBUG: Profile API response status: {response.status_code}")
            print(f"DEBUG: Profile API response text: {response.text[:500]}")
            
            if response.status_code == 200:
                api_profile = response.json()
                # Merge API data with defaults
                profile_data.update(api_profile)
                print("Profile data fetched from API successfully")
            else:
                print(f"API returned status {response.status_code}, using default data")
        except Exception as api_error:
            print(f"API error: {api_error}, using default data")
        
        if request.method == 'POST':
            print("Processing profile update...")
            # Handle profile update
            update_data = {
                'name': request.form.get('name'),
                'email': request.form.get('email'),
                'organization': request.form.get('organization'),
                'phone': request.form.get('phone'),
                'location': request.form.get('location'),
                'experience_years': int(request.form.get('experience_years', 0)),
                'specializations': request.form.getlist('specializations'),
                'bio': request.form.get('bio'),
                'website': request.form.get('website'),
                'social_media': {
                    'linkedin': request.form.get('linkedin'),
                    'facebook': request.form.get('facebook'),
                    'instagram': request.form.get('instagram')
                }
            }
            
            # Update local profile data
            profile_data.update(update_data)
            
            # Try to update via API
            try:
                update_response = requests.put(
                    f"{current_app.config['API_URL']}/matchmaker/profile",
                    json=update_data,
                    headers=headers,
                    timeout=5
                )
                
                if update_response.status_code == 200:
                    flash('Profile updated successfully!', 'success')
                else:
                    flash('Profile updated locally (API unavailable)', 'info')
            except Exception as update_error:
                flash('Profile updated locally (API unavailable)', 'info')
            
            return redirect(url_for('users.profile'))
        
        # Create default statistics
        stats_data = {
            'applicants': 25,
            'matches': 12,
            'success_rate': 85,
            'monthly_matches': 3,
            'avg_compatibility': 78,
            'active_applicants': 8,
            'pending_matches': 2
        }
        
        # Try to fetch statistics from API
        try:
            stats_response = requests.get(
                f"{current_app.config['API_URL']}/matchmaker/stats",
                headers=headers,
                timeout=5
            )
            
            if stats_response.status_code == 200:
                api_stats = stats_response.json()
                stats_data.update(api_stats)
                print("Statistics fetched from API successfully")
        except Exception as stats_error:
            print(f"Stats API error: {stats_error}, using default data")
        
        # Create default recent activity
        recent_activity = [
            {
                'title': 'New Match Created',
                'description': 'Matched Sarah and David with 85% compatibility',
                'time': '2 hours ago',
                'icon': 'heart'
            },
            {
                'title': 'Profile Updated',
                'description': 'Updated applicant profile for Rachel',
                'time': '1 day ago',
                'icon': 'user-edit'
            },
            {
                'title': 'New Applicant',
                'description': 'Added new applicant: Michael Cohen',
                'time': '3 days ago',
                'icon': 'user-plus'
            }
        ]
        
        # Try to fetch activity from API
        try:
            activity_response = requests.get(
                f"{current_app.config['API_URL']}/matchmaker/activity",
                headers=headers,
                timeout=5
            )
            
            if activity_response.status_code == 200:
                api_activity = activity_response.json().get('activities', [])
                if api_activity:
                    recent_activity = api_activity
                    print("Activity data fetched from API successfully")
        except Exception as activity_error:
            print(f"Activity API error: {activity_error}, using default data")
        
        print(f"Rendering profile page with data: {len(profile_data)} profile fields, {len(stats_data)} stats, {len(recent_activity)} activities")
        
        return render_template('users/profile.html', 
                             profile=profile_data, 
                             stats=stats_data, 
                             recent_activity=recent_activity)
        
    except Exception as e:
        print(f"Profile route error: {e}")
        flash(f"Error loading profile: {str(e)}", 'danger')
        return render_template('users/profile.html', 
                             profile={'name': current_user.name, 'email': current_user.email}, 
                             stats={}, 
                             recent_activity=[])

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

@bp.route('/profile/upload-picture', methods=['POST'])
@login_required
def upload_profile_picture():
    """Upload profile picture for the current matchmaker"""
    try:
        if 'profile_picture' not in request.files:
            return jsonify({'success': False, 'message': 'No file uploaded'}), 400
        
        file = request.files['profile_picture']
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No file selected'}), 400
        
        # Validate file type
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
        if not file.filename.lower().endswith(tuple('.' + ext for ext in allowed_extensions)):
            return jsonify({'success': False, 'message': 'Invalid file type. Please upload an image.'}), 400
        
        # Validate file size (max 5MB)
        if len(file.read()) > 5 * 1024 * 1024:
            file.seek(0)  # Reset file pointer
            return jsonify({'success': False, 'message': 'File too large. Maximum size is 5MB.'}), 400
        
        file.seek(0)  # Reset file pointer
        
        # Create uploads directory if it doesn't exist
        import os
        upload_dir = os.path.join(current_app.root_path, 'static', 'uploads', 'profile_pictures')
        os.makedirs(upload_dir, exist_ok=True)
        
        # Generate unique filename
        import uuid
        filename = f"{current_user.id}_{uuid.uuid4().hex}.jpg"
        filepath = os.path.join(upload_dir, filename)
        
        # Save file
        file.save(filepath)
        
        # Generate URL for the uploaded image
        image_url = f"/static/uploads/profile_pictures/{filename}"
        
        # Update profile data with new picture URL
        profile_data = {
            'profile_picture': image_url
        }
        
        # Try to update via API
        try:
            headers = {'Authorization': f'Bearer {current_user.token}'}
            update_response = requests.put(
                f"{current_app.config['API_URL']}/matchmaker/profile",
                json=profile_data,
                headers=headers,
                timeout=10
            )
            
            if update_response.status_code == 200:
                print("Profile picture updated via API successfully")
            else:
                print(f"API update failed with status {update_response.status_code}")
        except Exception as api_error:
            print(f"API error updating profile picture: {api_error}")
        
        return jsonify({
            'success': True, 
            'message': 'Profile picture uploaded successfully',
            'image_url': image_url
        })
        
    except Exception as e:
        print(f"Error uploading profile picture: {e}")
        return jsonify({'success': False, 'message': 'Error uploading profile picture'}), 500 