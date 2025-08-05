from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt, create_access_token  # We use get_jwt() if needed directly
from flask import request
from app.services.facade import HBnBFacade
from app.utils.decorators import admin_required

ns = Namespace('users', description='User operations')

# Model for user registration
user_registration_model = ns.model('UserRegistration', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email address of the user'),
    'password': fields.String(required=True, description='Password for the user')
})

# Model for user profile update (users can only update their own profile)
user_update_model = ns.model('UserUpdate', {
    'first_name': fields.String(required=False, description='Updated first name of the user'),
    'last_name': fields.String(required=False, description='Updated last name of the user'),
    'email': fields.String(required=False, description='Updated email address'),
    'password': fields.String(required=False, description='Updated password')
})

@ns.route('/')
class UserList(Resource):
    @ns.expect(user_registration_model, validate=True)
    @ns.response(200, 'User successfully registered with access token')
    @ns.response(400, 'Invalid input data or email already registered')
    def post(self):
        """Create a new user (open registration)."""
        facade = HBnBFacade()
        user_data = ns.payload
        
        # Check if a user with this email already exists
        if facade.get_user_by_email(user_data['email']):
            return {'error': 'Email already registered'}, 400
        
        # Force new users to be normal users (not admin)
        user_data['is_admin'] = False
        
        try:
            new_user = facade.create_user(user_data)
            
            # Generate JWT token for the newly created user
            access_token = create_access_token(
                identity=str(new_user.id),
                additional_claims={'is_admin': new_user.is_admin}
            )
            
            return {
                'id': new_user.id, 
                'message': 'User successfully registered',
                'access_token': access_token
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @jwt_required()
    def get(self):
        """Retrieve a list of all users (Admin only)."""
        facade = HBnBFacade()
        users = facade.get_all_users()
        return users, 200



@ns.route('/<string:user_id>')
class UserResource(Resource):
    @jwt_required()
    @ns.expect(user_update_model, validate=True)
    @ns.response(200, 'User updated successfully')
    @ns.response(400, 'Email already in use or invalid input')
    @ns.response(403, 'Unauthorized action')
    @ns.response(404, 'User not found')
    def put(self, user_id):
        """
        Update user details (users can only update their own profile).
        """
        claims = get_jwt()
        facade = HBnBFacade()
        user = facade.get_user_by_id(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        # Users can only update their own profile, unless they are admin
        if not claims.get('is_admin') and claims.get('sub') != user_id:
            return {'error': 'Unauthorized action'}, 403

        update_data = ns.payload

        # If email is provided, check if it's already used by another user.
        if 'email' in update_data:
            existing_user = facade.get_user_by_email(update_data['email'])
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email is already in use'}, 400

        try:
            updated_user = facade.update_user(user_id, update_data)
            return {'message': 'User updated successfully', 'user': updated_user.to_dict()}, 200
        except Exception as e:
            return {'error': str(e)}, 400

    @jwt_required()
    @ns.response(200, 'User deleted successfully')
    @ns.response(404, 'User not found')
    def delete(self, user_id):
        """(Admin Only) Delete a user."""
        facade = HBnBFacade()
        if not facade.get_user_by_id(user_id):
            return {'error': 'User not found'}, 404

        deletion_result = facade.user_repository.delete(user_id)
        if deletion_result:
            return {'message': 'User deleted successfully'}, 200
        else:
            return {'error': 'Failed to delete user'}, 400

    @jwt_required()
    def get(self, user_id):
        """Retrieve a specific user (users can only view their own profile)."""
        claims = get_jwt()
        facade = HBnBFacade()
        user = facade.get_user_by_id(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        # Users can only view their own profile, unless they are admin
        if not claims.get('is_admin') and claims.get('sub') != user_id:
            return {'error': 'Unauthorized action'}, 403
            
        return user.to_dict(), 200
