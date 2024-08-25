from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models.User import User

class UserController:

    def register(self):
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if user:
            return jsonify({"message": "User already exists"}), 400

        new_user = User(
            name=data['name'],
            email=data['email'],
            phone=data.get('phone')
        )
        new_user.set_password(data['password'])
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User registered successfully"}), 201

    def login(self):
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()

        if user and user.check_password(data['password']):
            token = user.generate_jwt()
            return jsonify({"token": token}), 200

        return jsonify({"message": "Invalid credentials"}), 401

    @jwt_required()
    def update(self):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if not user:
            return jsonify({"message": "User not found"}), 404

        data = request.get_json()
        user.name = data.get('name', user.name)
        user.email = data.get('email', user.email)
        user.phone = data.get('phone', user.phone)

        if 'password' in data:
            user.set_password(data['password'])

        db.session.commit()

        return jsonify({"message": "User data updated successfully"}), 200

    @jwt_required()
    def delete(self):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if not user:
            return jsonify({"message": "User not found"}), 404

        db.session.delete(user)
        db.session.commit()

        return jsonify({"message": "User account deleted successfully"}), 200
