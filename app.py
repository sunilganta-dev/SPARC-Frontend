from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_login import LoginManager, current_user
import os
import datetime
import requests
from dotenv import load_dotenv
from models.user import User

# ---------------------------------------------------------
# Load environment variables
# ---------------------------------------------------------
load_dotenv()

# ---------------------------------------------------------
# Initialize Flask app
# ---------------------------------------------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['API_URL'] = os.getenv('API_URL', 'https://sparc.chaya.dev/api')

# Folder for uploaded applicant pictures
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, "static/uploads/profile_pictures")
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ---------------------------------------------------------
# Setup login manager
# ---------------------------------------------------------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    """Load user from session if logged in."""
    if 'user_data' in session:
        user_data = session['user_data']
        if str(user_data.get('id')) == str(user_id):
            return User(
                id=user_data.get('id'),
                email=user_data.get('email'),
                name=user_data.get('name'),
                token=user_data.get('token')
            )
    return None

# ---------------------------------------------------------
# Template context processors
# ---------------------------------------------------------
@app.context_processor
def inject_now():
    """Provide `now` datetime globally in templates."""
    return {'now': datetime.datetime.now()}

# ---------------------------------------------------------
# Import and register routes
# ---------------------------------------------------------
from routes import auth_routes, user_routes, match_routes
from routes.applicant_routes import applicant_public_bp   # public applicant form

app.register_blueprint(auth_routes.bp)
app.register_blueprint(user_routes.bp)
app.register_blueprint(match_routes.bp)
app.register_blueprint(applicant_public_bp, url_prefix="/apply")

# ---------------------------------------------------------
# Home page route
# ---------------------------------------------------------
@app.route('/')
def index():
    """Landing page with stats (fetched from backend if logged in)."""
    stats = {'applicants': 0, 'matches': 0, 'recent': 0}

    if current_user.is_authenticated:
        try:
            headers = {'Authorization': f'Bearer {current_user.token}'}
            response = requests.get(
                f"{app.config['API_URL']}/matchmaker/stats",
                headers=headers
            )
            if response.status_code == 200:
                stats = response.json()
        except requests.exceptions.RequestException:
            flash("⚠️ Could not fetch stats from backend.", "warning")

    return render_template('index.html', stats=stats)

# ---------------------------------------------------------
# Run app
# ---------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5006)
