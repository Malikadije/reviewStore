from flask import Blueprint, request, jsonify, redirect, url_for, render_template
from flask_jwt_extended import create_access_token, jwt_required
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from app.models import User, Review

user_bp = Blueprint('user', __name__)

# User Registration
@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    role = data.get('role')

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    existing_user = User.get_user_by_email(email)
    if existing_user:
        return jsonify({"message": "User already exists"}), 400

    User.create_user(username, password, email, role)
    return jsonify({"message": "User created successfully"}), 201

# User Login
@user_bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = User.get_user_by_email(email)
        # Check if user exists and verify password
        if not user or not User.verify_password(user.password_hash, password):
            return jsonify({"message": "Invalid email or password"}), 401
        
        # Log the user in
        login_user(user)
        
        # Create JWT token with user details
        access_token = create_access_token(identity={'username': user.username, 'role': user.role})
        
        return jsonify(access_token=access_token), 200
    return render_template('login.html');

# Get All Reviews
@user_bp.route('/', methods=['GET'])
def home():
    return redirect(url_for('admin.get_reviews'))

# Create a Review
@user_bp.route('/reviews', methods=['POST'])
# @jwt_required()
def create_review():
    data = request.get_json()
    content = data.get('content')
    rating = data.get('rating')
    user_id = data.get('user_id')  # This should ideally be obtained from the JWT

    if not content or not rating:
        return jsonify({"message": "Title, content, and rating are required"}), 400

    Review.create_review(user_id, content, rating)
    return jsonify({"message": "Review created successfully"}), 201