from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, email, name, token):
        self.id = id
        self.email = email
        self.name = name
        self.token = token
    
    @staticmethod
    def get(user_id):
        # This method is required by Flask-Login but
        # in this case, we're using a JWT token-based approach
        # so we'll return None (users are loaded from the backend)
        return None 