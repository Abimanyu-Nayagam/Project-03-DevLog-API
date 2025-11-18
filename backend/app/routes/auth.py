from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from app.models.db_models import User, db
from app.models.models import CreateUserRequest
from flask_jwt_extended import JWTManager, create_access_token
from re import match

bcrypt = Bcrypt()
jwt = JWTManager()

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    if not email:
        return jsonify({"error": "Email is required"}), 400
    if not match(r'^[\w\. ]+@[\w\. ]+\.\w+$', email):
        return jsonify({"error": "Enter a valid email address"}), 400
    if not username:
        return jsonify({"error": "Username is required"}), 400
    if not password:
        return jsonify({"error": "Password is required"}), 400

    try:
        new_user_data = CreateUserRequest(email=email, username=username, password=password)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    # Check if user already exists
    existing_user = User.query.filter((User.email == email) | (User.username == username)).first()
    if existing_user:
        return jsonify({"error": "User with this email or username already exists"}), 409
    
    # Hash the password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Create new user
    new_user = User(username=username, email=email, password_hashed=hashed_password)

    # Add to database
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": f"User {username} registered successfully!"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username:
        return jsonify({"error": "Username is required"}), 400
    if not password:
        return jsonify({"error": "Password is required"}), 400

    # Find user by username
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User of that username does not exist"}), 401

    # Verify user exists and password is correct
    if user and bcrypt.check_password_hash(user.password_hashed, password):
        # Create JWT access token
        access_token = create_access_token(identity=str(user.id))
        return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'username': user.username
        }), 200
    else:
        return jsonify({'message': 'Incorrect password'}), 401
