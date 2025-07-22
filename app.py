from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import os
from dotenv import load_dotenv
import requests
from models.user import User
import datetime

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['API_URL'] = os.getenv('API_URL', 'http://localhost:5000/api')

# Setup login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    # Check if we have the user data in the session
    if 'user_data' in session:
        user_data = session['user_data']
        # Only return a user if the ID matches
        if str(user_data.get('id')) == str(user_id):
            return User(
                id=user_data.get('id'),
                email=user_data.get('email'),
                name=user_data.get('name'),
                token=user_data.get('token')
            )
    return None

# Context processor for templates
@app.context_processor
def inject_now():
    return {'now': datetime.datetime.now()}

# Import routes
from routes import auth_routes, user_routes, match_routes

# Register Blueprints
app.register_blueprint(auth_routes.bp)
app.register_blueprint(user_routes.bp)
app.register_blueprint(match_routes.bp)

@app.route('/')
def index():
    # Pass some basic stats to the home page
    stats = {
        'applicants': 0,
        'matches': 0,
        'recent': 0
    }
    
    # If user is logged in, try to fetch real stats
    if current_user.is_authenticated:
        try:
            headers = {'Authorization': f'Bearer {current_user.token}'}
            response = requests.get(
                f"{app.config['API_URL']}/matchmaker/stats",
                headers=headers
            )
            
            if response.status_code == 200:
                stats = response.json()
        except:
            # Fail silently if API is not available
            pass
    
    return render_template('index.html', stats=stats)

if __name__ == '__main__':
    app.run(debug=True, port=5001) 