from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})


@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        amenity_data = api.payload
        try:
            if not amenity_data['name'] or len(amenity_data['name']) > 50:
                return {'error':
                        'Amenity name must be a string of 1 to 50 characters.'
                        }, 400
            existing_amenity = facade.get_amenity_by_name(
                amenity_data['name'])
            if existing_amenity:
                return {'error': 'Amenity already registered'}, 400
            new_amenity = facade.create_amenity(amenity_data)
            return {'id': new_amenity.id, 'name': new_amenity.name}, 201
        except Exception as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return [{'id': amenity.id, 'name': amenity.name}
                for amenity in amenities], 200


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'amenity details retrieved successfully')
    @api.response(404, 'amenity not found')
    def get(self, amenity_id):
        '''Get amenity details with ID'''
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'amenity not found'}, 404
        return {'id': amenity.id, 'name': amenity.name}, 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        '''Update amenity details with ID'''
        amenity_data = api.payload
        try:
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
            return {'id': updated_amenity.id, 'name': updated_amenity.name
                    }, 200
        except ValueError as e:
            return {'error': str(e)}, 400
