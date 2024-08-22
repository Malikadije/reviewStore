from flask import Blueprint, request, jsonify, redirect, url_for, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from app.models import Review
from app.models import User

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('user.login'))

@admin_bp.route('/users/<int:user_id>/delete', methods=['DELETE'])
@login_required
def delete_user(user_id):
    if current_user.role != 'admin':
        return jsonify({"message": "Forbidden"}), 403
    User.delete_user(user_id)
    return jsonify({"message": "User deleted successfully"}), 200


@admin_bp.route('/users/<int:user_id>/details', methods=['GET'])
@login_required
def details_user(user_id):
    if current_user.role != 'admin':
        return jsonify({"message": "Forbidden"}), 403
    user = User.get_user_by_id(user_id)
    return jsonify(username=user.username,role=user.role,email=user.email,id=user_id), 200

@admin_bp.route('/users/update', methods=['POST'])
@login_required
def update_user():
    if current_user.role != 'admin':
        return jsonify({"message": "Forbidden"}), 403
    
    data = request.get_json()
    user_id = int(data.get('userId'))
    username = data.get('username')
    email = data.get('email')
    role = data.get('role')
    password = current_user.password_hash

    User.update_user(user_id, username, email, role, password)
    return jsonify({"message": "User updated successfully"}), 200


# Get Reviews
@admin_bp.route('/user_list', methods=['GET'])
# @jwt_required()
def get_user_list():
    users = User.get_all_users()
    return jsonify(users), 200

# Get Reviews
@admin_bp.route('/reviews', methods=['GET'])
@login_required
def get_reviews():
    reviews = Review.get_all_reviews()
    user_info = {
        'id': current_user.id,
        'username': current_user.username,
        'email': current_user.email,
        'role': current_user.role
    }
    return render_template('admin.html', reviews=reviews, user=user_info)

# Get Reviews
@admin_bp.route('/review_list', methods=['GET'])
@login_required
def get_reviews_list():
    reviews = Review.get_all_reviews()
    return jsonify(reviews), 200

# Get Review by ID
@admin_bp.route('/reviews/<int:review_id>', methods=['GET'])
@login_required
def get_review(review_id):
    review = Review.get_review_by_id(review_id)
    if not review:
        return jsonify({"message": "Review not found"}), 404
    return jsonify(review), 200

# Update a Review
@admin_bp.route('/reviews/<int:review_id>/update', methods=['POST'])
@login_required
def update_review(review_id):
    data = request.get_json()
    content = data.get('content')
    rating = data.get('rating')

    if not content or not rating:
        return jsonify({"message": "Title, content, and rating are required"}), 400

    Review.update_review(review_id, content, rating)
    return jsonify({"message": "Review updated successfully"}), 200

# Delete a Review
@admin_bp.route('/reviews/<int:review_id>/delete', methods=['POST'])
# @jwt_required()
def delete_review(review_id):
    Review.delete_review(review_id)
    return jsonify({"message": "Review deleted successfully"}), 200
