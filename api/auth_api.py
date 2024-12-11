from flask import request  # Import request to access incoming request data
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from domain import User  # Ensure this imports all necessary models
from db import Session, revoked_tokens  # Import the Session and revoked_tokens from db.py

auth_ns = Namespace('auth', description='Authentication operations')
user_model = auth_ns.model('User', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password')
})

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(user_model)
    def post(self):
        data = request.get_json()
        session = Session()
        user = session.query(User).filter_by(username=data['username']).first()
        session.close()
        if user and user.check_password(data['password']):
            access_token = create_access_token(identity={'id': user.id, 'username': user.username})
            return {'access_token': access_token}, 200
        else:
            return {'message': 'Invalid credentials'}, 401

@auth_ns.route('/logout')
class Logout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        revoked_tokens[jti] = True
        print(f"Token with JTI {jti} has been revoked. Current revoked tokens: {revoked_tokens}")  # Debugging line
        return {'message': 'Token has been revoked'}, 200

@auth_ns.route('/protected')
class Protected(Resource):
    @auth_ns.doc(security='Bearer Auth')
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        return {'logged_in_as': current_user}, 200 