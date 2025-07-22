from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True,
                             description='Latitude of the place'),
    'longitude': fields.Float(required=True,
                              description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True,
                             description="List of amenities ID's")
})

def validate_place_data(data):
    """Validate place data."""
    if 'price' in data:
        try:
            price = float(data['price'])
            if price <= 0:
                return {'error': 'Price must be a positive number'}, 400
        except ValueError:
            return {'error': 'Price must be a float'}, 400

    if 'latitude' in data:
        try:
            latitude = float(data['latitude'])
            if not (-90.0 <= latitude <= 90.0):
                return {'error': 'Latitude must be between -90.0 and 90.0'}, 400
        except ValueError:
            return {'error': 'Latitude must be a float'}, 400

    if 'longitude' in data:
        try:
            longitude = float(data['longitude'])
            if not (-180.0 <= longitude <= 180.0):
                return {'error': 'Longitude must be between -180.0 and 180.0'}, 400
        except ValueError:
            return {'error': 'Longitude must be a float'}, 400

    return None

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        data = api.payload
        validation_error = validate_place_data(data)
        if validation_error:
            return validation_error

        title = data.get('title')
        description = data.get('description')
        price = data.get('price')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        owner_id = data.get('owner_id')
        amenities = data.get('amenities', [])

        try:
            new_place = facade.create_place(title, description, price,
                                            latitude,
                                            longitude, owner_id, amenities)
            return new_place.to_dict(), 201
        except ValueError as e:
            api.abort(400, 'Failed to create place: ' + str(e))
        except TypeError as e:
            api.abort(400, 'Invalid input data: ' + str(e))

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        try:
            places = facade.get_all_places()
            return [place.to_dict() for place in places], 200
        except ValueError as e:
            api.abort(404, str(e))


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        try:
            place = facade.get_place(place_id)
            return place.to_dict(), 200
        except ValueError as e:
            api.abort(404, str(e))

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        data = api.payload
        validation_error = validate_place_data(data)
        if validation_error:
            return validation_error

        try:
            updated_place = facade.update_place(place_id, data)
            return updated_place.to_dict(), 200
        except ValueError as e:
            api.abort(400, str(e))
        except KeyError as e:
            api.abort(404, str(e))
