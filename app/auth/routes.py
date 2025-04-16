from flask import Blueprint, jsonify, request
from .schemas import LoginSchema, UserSchema
from app.extensions import db
from app.models import User
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError


auth_bp = Blueprint('auth', __name__)
user_schema = UserSchema()
login_schema = LoginSchema()


@auth_bp.route('/')
def home():
    """A function to display the default page"""
    return "Hello world, I want to create my notes app"

@auth_bp.route('/register', methods=['POST'])  #The route can only accept POST request
def register_users():
    """A function to register users and save them to the db"""
    try:
        data = user_schema.load(request.json)  #validate and deserializes(converts json to python dict) data from the request body
        new_user = User(name=data['name'], email=data['email']) #Just like raw SQL queries, you indicate the values being input into the columns
        new_user.password = data['password']
        print(new_user.password_hash)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({
            "status": "Success",
            "message": "User registered successfully",
            "user": { "id":new_user.id, "name": new_user.name, "email":new_user.email }
        }), 201
    
    except ValidationError as err:
        return jsonify({"status":"error", "message": err.messages}), 400
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"status":"error", "message": "Email already exists"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"status":"error", "message": "Unexpected error occurred"}), 500

@auth_bp.route('/login', methods=['POST'])
def login_users():
    """A function to login users using email and password"""
    try:
        data = login_schema.load(request.json)
        user = User.query.filter_by(email=data['email']).first()
        if not user or not user.check_password(data['password']):
            return jsonify({"status": "error", "message": "Incorrect email or password"}), 401
        
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))

        return jsonify({
            "status": "success", 
            "message": "Login Successful",
            "access_token": access_token, 
            "refresh_token": refresh_token})
    
    except ValidationError as err:
        return jsonify({"status": "error", "message": err.messages}), 400
    except Exception as e:
        db.session.rollback()
        print(f"Unexpected error: {e}")
        return jsonify({"status": "error", "message": "Unexpected error occurred"}), 500

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if user:
        return jsonify({"id": user.id, "name": user.name, "email": user.email})
    return jsonify({"error": "User not found"}), 404