from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify
from flask_login import login_required, current_user
import requests

bp = Blueprint('matches', __name__, url_prefix='/matches')

@bp.route('/')
@login_required
def index():
    try:
        # Fetch all matches for the matchmaker's users
        headers = {'Authorization': f'Bearer {current_user.token}'}
        
        # Get optional limit parameter
        limit = request.args.get('limit', 100)
        
        response = requests.get(
            f"{current_app.config['API_URL']}/matchmaker/matches",
            params={'limit': limit},
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            print("Matchmaker matches data:", data)
            
            # Transform the data to match what our template expects
            transformed_matches = []
            
            # Handle different response formats
            if isinstance(data, list):
                match_list = data
            elif isinstance(data, dict) and 'matches' in data:
                match_list = data['matches']
            else:
                match_list = []
                
            for match in match_list:
                try:
                    # Skip if match is not a dictionary
                    if not isinstance(match, dict):
                        print(f"Skipping non-dict match: {match}")
                        continue
                        
                    # Get required fields safely
                    applicant_id = match.get('applicant_id', 0)
                    applicant_name = match.get('applicant_name', 'Unknown')
                    match_id = match.get('match_id', 0)
                    match_name = match.get('match_name', 'Unknown')
                    score = match.get('score', 0)
                    
                    # Create basic user objects
                    user_a = {
                        'id': applicant_id,
                        'name': applicant_name,
                        'first_name': applicant_name.split(' ')[0] if ' ' in applicant_name else applicant_name,
                        'last_name': applicant_name.split(' ')[1] if ' ' in applicant_name else '',
                        'age': match.get('applicant_age', 0),
                        'current_location': match.get('applicant_location', 'Unknown'),
                        'gender': match.get('applicant_gender', 'Unknown')
                    }
                    
                    user_b = {
                        'id': match_id,
                        'name': match_name,
                        'first_name': match_name.split(' ')[0] if ' ' in match_name else match_name,
                        'last_name': match_name.split(' ')[1] if ' ' in match_name else '',
                        'age': match.get('match_age', 0),
                        'current_location': match.get('match_location', 'Unknown'),
                        'gender': match.get('match_gender', 'Unknown')
                    }
                    
                    # Get compatibility data if available
                    compatibility = {}
                    if 'compatibility' in match and isinstance(match['compatibility'], dict):
                        compatibility = match['compatibility']
                    
                    # Create a transformed match object
                    transformed_match = {
                        'compatibility_score': score,
                        'score': score,
                        'user_a': user_a,
                        'user_b': user_b,
                        'compatibility': compatibility,
                        'date_created': match.get('date_created', 'Recent')
                    }
                    transformed_matches.append(transformed_match)
                except Exception as e:
                    print(f"Error processing match: {e}")
                    continue
            
            return render_template('matches/index.html', matches=transformed_matches)
        else:
            print(response.json())
            flash('Failed to retrieve matches.', 'danger')
            return render_template('matches/index.html', matches=[])
    except Exception as e:
        import traceback
        traceback.print_exc()
        flash(f"Connection error: {str(e)}", 'danger')
        return render_template('matches/index.html', matches=[])

@bp.route('/user/<int:user_id>')
@login_required
def user_matches(user_id):
    try:
        # Fetch matches for a specific user
        headers = {'Authorization': f'Bearer {current_user.token}'}
        
        # Get optional limit parameter
        limit = request.args.get('limit', 10)
        
        response = requests.get(
            f"{current_app.config['API_URL']}/user/{user_id}/matches",
            params={'limit': limit},
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            print("User matches data:", data)
            
            # Transform the data to match what our template expects
            transformed_matches = []
            
            # Handle different response formats
            if isinstance(data, list):
                match_list = data
            elif isinstance(data, dict) and 'matches' in data:
                match_list = data['matches']
            else:
                match_list = []
                
            for match in match_list:
                try:
                    # Skip if match is not a dictionary
                    if not isinstance(match, dict):
                        print(f"Skipping non-dict match: {match}")
                        continue
                        
                    # Get required fields safely
                    applicant_name = match.get('applicant_name', 'Unknown')
                    match_id = match.get('match_id', 0)
                    match_name = match.get('match_name', 'Unknown')
                    score = match.get('score', 0)
                    
                    # Create basic user objects
                    user_a = {
                        'id': user_id,  # This is the current user we're viewing
                        'name': applicant_name,
                        'first_name': applicant_name.split(' ')[0] if ' ' in applicant_name else applicant_name,
                        'last_name': applicant_name.split(' ')[1] if ' ' in applicant_name else '',
                        'age': match.get('applicant_age', 0),
                        'current_location': match.get('applicant_location', 'Unknown'),
                        'gender': match.get('applicant_gender', 'Unknown')
                    }
                    
                    user_b = {
                        'id': match_id,
                        'name': match_name,
                        'first_name': match_name.split(' ')[0] if ' ' in match_name else match_name,
                        'last_name': match_name.split(' ')[1] if ' ' in match_name else '',
                        'age': match.get('match_age', 0),
                        'current_location': match.get('match_location', 'Unknown'),
                        'gender': match.get('match_gender', 'Unknown')
                    }
                    
                    # Get compatibility data if available
                    compatibility = {}
                    if 'compatibility' in match and isinstance(match['compatibility'], dict):
                        compatibility = match['compatibility']
                    
                    # Create a transformed match object
                    transformed_match = {
                        'compatibility_score': score,
                        'score': score,
                        'user_a': user_a,
                        'user_b': user_b,
                        'compatibility': compatibility,
                        'date_created': match.get('date_created', 'Recent')
                    }
                    transformed_matches.append(transformed_match)
                except Exception as e:
                    print(f"Error processing match: {e}")
                    continue
            
            # Get user details
            user_response = requests.get(
                f"{current_app.config['API_URL']}/user/{user_id}",
                headers=headers
            )
            
            if user_response.status_code == 200:
                user = user_response.json()
                # Ensure user has all required fields
                processed_user = ensure_user_fields(user, user_id)
                return render_template('matches/user_matches.html', matches=transformed_matches, user=processed_user)
            else:
                flash('User not found or access denied.', 'danger')
                return redirect(url_for('matches.index'))
        else:
            flash('Failed to retrieve matches.', 'danger')
            return redirect(url_for('matches.index'))
    except Exception as e:
        import traceback
        traceback.print_exc()
        flash(f"Connection error: {str(e)}", 'danger')
        return redirect(url_for('matches.index'))

@bp.route('/compatibility/<int:user_a_id>/<int:user_b_id>')
@login_required
def compatibility(user_a_id, user_b_id):
    try:
        # Fetch detailed compatibility between two users
        headers = {'Authorization': f'Bearer {current_user.token}'}
        response = requests.get(
            f"{current_app.config['API_URL']}/matches/compatibility/{user_a_id}/{user_b_id}",
            headers=headers
        )
        
        if response.status_code == 200:
            compatibility_data = response.json()
            print("Compatibility data:", compatibility_data)
            
            # Transform compatibility data to fit our template
            transformed_compatibility = {
                'overall_score': 0,
                'score': 0,
                'factors': []
            }
            
            # Handle different response formats
            if isinstance(compatibility_data, dict):
                # Set the overall score
                if 'score' in compatibility_data:
                    transformed_compatibility['overall_score'] = compatibility_data['score']
                    transformed_compatibility['score'] = compatibility_data['score']
                
                # Extract factors if available
                if 'compatibility' in compatibility_data and isinstance(compatibility_data['compatibility'], dict):
                    # Prepare factors from compatibility details
                    factors = []
                    for category, details in compatibility_data['compatibility'].items():
                        if isinstance(details, dict) and 'score' in details:
                            factor = {
                                'name': category.replace('_', ' ').title(),
                                'score': details['score'],
                                'weight': details.get('weight', 1),
                                'notes': ''
                            }
                            
                            # Add details as notes if available
                            if 'details' in details and isinstance(details['details'], dict):
                                notes = []
                                for key, value in details['details'].items():
                                    notes.append(f"{key}: {value}")
                                factor['notes'] = '; '.join(notes)
                                
                            factors.append(factor)
                    
                    transformed_compatibility['factors'] = factors
            
            # Get user A details
            user_a_response = requests.get(
                f"{current_app.config['API_URL']}/user/{user_a_id}",
                headers=headers
            )
            
            # Get user B details
            user_b_response = requests.get(
                f"{current_app.config['API_URL']}/user/{user_b_id}",
                headers=headers
            )
            
            if user_a_response.status_code == 200 and user_b_response.status_code == 200:
                user_a = user_a_response.json()
                user_b = user_b_response.json()
                
                # Ensure user objects have required fields
                user_a_processed = ensure_user_fields(user_a, user_a_id)
                user_b_processed = ensure_user_fields(user_b, user_b_id)
                
                print("User A:", user_a_processed)
                print("User B:", user_b_processed)
                
                return render_template(
                    'matches/compatibility.html',
                    compatibility=transformed_compatibility,
                    user_a=user_a_processed,
                    user_b=user_b_processed
                )
            else:
                flash('One or both users not found or access denied.', 'danger')
                return redirect(url_for('matches.index'))
        else:
            flash('Failed to retrieve compatibility data.', 'danger')
            return redirect(url_for('matches.index'))
    except Exception as e:
        flash(f"Connection error: {str(e)}", 'danger')
        return redirect(url_for('matches.index'))

def ensure_user_fields(user_data, user_id):
    """Ensure user object has all required fields"""
    if isinstance(user_data, str):
        # If user_data is a string, create a basic user object
        return {
            'id': user_id,
            'name': user_data,
            'first_name': user_data,
            'last_name': '',
            'age': 0,
            'gender': 'Unknown',
            'current_location': 'Unknown'
        }
    
    # Start with the original data
    processed_user = user_data.copy() if isinstance(user_data, dict) else {'id': user_id}
    
    # Ensure ID is present
    if 'id' not in processed_user:
        processed_user['id'] = user_id
    
    # Ensure name is present
    if 'name' not in processed_user:
        if 'first_name' in processed_user and 'last_name' in processed_user:
            processed_user['name'] = f"{processed_user['first_name']} {processed_user['last_name']}"
        else:
            processed_user['name'] = f"User {user_id}"
    
    # Ensure first_name and last_name are present
    if 'first_name' not in processed_user:
        if ' ' in processed_user.get('name', ''):
            processed_user['first_name'] = processed_user['name'].split(' ')[0]
        else:
            processed_user['first_name'] = processed_user.get('name', f"User {user_id}")
    
    if 'last_name' not in processed_user:
        if ' ' in processed_user.get('name', ''):
            processed_user['last_name'] = processed_user['name'].split(' ')[1]
        else:
            processed_user['last_name'] = ''
    
    # Ensure other fields are present
    if 'age' not in processed_user:
        processed_user['age'] = 0
    
    if 'gender' not in processed_user:
        processed_user['gender'] = 'Unknown'
    
    if 'current_location' not in processed_user:
        # Check for city and country
        if 'city' in processed_user and 'country' in processed_user:
            processed_user['current_location'] = f"{processed_user['city']}, {processed_user['country']}"
        else:
            processed_user['current_location'] = 'Unknown'
    
    return processed_user

@bp.route('/all')
@login_required
def all_matches():
    try:
        # Fetch all top matches across the system (admin only)
        headers = {'Authorization': f'Bearer {current_user.token}'}
        
        # Get optional parameters
        limit_per_match = request.args.get('limit_per_match', 5)
        min_score = request.args.get('min_score', 50)
        
        response = requests.get(
            f"{current_app.config['API_URL']}/matches/all",
            params={
                'limit_per_match': limit_per_match,
                'min_score': min_score
            },
            headers=headers
        )
        
        if response.status_code == 200:
            all_matches = response.json()
            return render_template('matches/all_matches.html', matches=all_matches)
        elif response.status_code == 403:
            flash('Access denied. Admin privileges required.', 'danger')
            return redirect(url_for('matches.index'))
        else:
            flash('Failed to retrieve matches.', 'danger')
            return redirect(url_for('matches.index'))
    except Exception as e:
        flash(f"Connection error: {str(e)}", 'danger')
        return redirect(url_for('matches.index')) 