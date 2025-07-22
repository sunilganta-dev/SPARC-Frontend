from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, session
from flask_login import login_user, logout_user, login_required, current_user
import requests
from models.user import User
from forms.auth_forms import LoginForm, RegisterForm, PasswordResetForm

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        try:
            # Make API request to backend for authentication
            response = requests.post(
                f"{current_app.config['API_URL']}/auth/login",
                json={
                    'email': form.email.data,
                    'password': form.password.data
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                # Store user data in session
                session['user_data'] = {
                    'id': data['matchmaker']['id'],
                    'email': data['matchmaker']['email'],
                    'name': data['matchmaker']['name'],
                    'token': data['token']
                }
                # Create a user object and log them in
                user = User(
                    id=data['matchmaker']['id'],
                    email=data['matchmaker']['email'],
                    name=data['matchmaker']['name'],
                    token=data['token']
                )
                login_user(user)
                next_page = request.args.get('next', url_for('index'))
                return redirect(next_page)
            else:
                error_msg = response.json().get('message', 'Invalid email or password')
                flash(error_msg, 'danger')
        except Exception as e:
            flash(f"Connection error: {str(e)}", 'danger')
    
    return render_template('auth/login.html', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            # Make API request to backend for registration
            response = requests.post(
                f"{current_app.config['API_URL']}/auth/register",
                json={
                    'email': form.email.data,
                    'password': form.password.data,
                    'name': form.name.data
                }
            )
            
            if response.status_code == 201:
                flash('Registration successful! Please log in.', 'success')
                return redirect(url_for('auth.login'))
            else:
                error_msg = response.json().get('message', 'Registration failed')
                flash(error_msg, 'danger')
        except Exception as e:
            flash(f"Connection error: {str(e)}", 'danger')
    
    return render_template('auth/register.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    # Clear user data from session
    session.pop('user_data', None)
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

@bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    form = PasswordResetForm()
    if form.validate_on_submit():
        try:
            # Make API request to backend for password reset
            response = requests.post(
                f"{current_app.config['API_URL']}/auth/reset-password",
                json={'email': form.email.data}
            )
            
            if response.status_code == 200:
                reset_info = response.json()
                # In a real app, we would just show a message
                # Here we're showing the token for demo purposes
                if 'token' in reset_info:
                    flash(f"Password reset initiated. For demo purposes, here's your token: {reset_info['token']}", 'info')
                else:
                    flash('Password reset instructions have been sent to your email.', 'info')
                return redirect(url_for('auth.login'))
            else:
                error_msg = response.json().get('message', 'Password reset failed')
                flash(error_msg, 'danger')
        except Exception as e:
            flash(f"Connection error: {str(e)}", 'danger')
    
    return render_template('auth/reset_password.html', form=form) 