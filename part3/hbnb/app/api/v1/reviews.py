from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from app.services.facade import HBnBFacade

ns = Namespace('reviews', description='Review operations')

review_model = ns.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place')
})

update_review_model = ns.model('UpdateReview', {
    'text': fields.String(required=False, description='Updated text of the review', nullable=False),
    'rating': fields.Integer(required=False, description='Updated rating (1-5)', nullable=False)
})

@ns.route('/')
class ReviewList(Resource):
    @jwt_required()
    @ns.expect(review_model, validate=True)
    @ns.response(201, 'Review successfully created')
    @ns.response(400, 'Invalid input data or review not allowed')
    def post(self):
        claims = get_jwt()
        review_data = ns.payload

        if 'sub' in claims:
            review_data['user_id'] = claims['sub']
        else:
            return {'error': 'User ID not found in token claims'}, 400

        facade = HBnBFacade()
        place = facade.get_place(review_data['place_id'])
        if not place:
            return {'error': 'Place not found'}, 404
        if place.get('owner', {}).get('id') == claims['sub']:
            return {'error': 'You cannot review your own place.'}, 400

        existing_reviews = facade.get_reviews_by_place(review_data['place_id'])
        for review in existing_reviews:
            if review.user.id == claims['sub']:
                return {'error': 'You have already reviewed this place.'}, 400

        try:
            new_review = facade.create_review(review_data)
            return {
                "id": new_review.id,
                "text": new_review.text,
                "rating": new_review.rating,
                "user_id": new_review.user.id,
                "place_id": new_review.place.id
            }, 201
        except ValueError as e:
            return {"error": str(e)}, 400

    @ns.response(200, 'List of reviews retrieved successfully')
    def get(self):
        facade = HBnBFacade()
        reviews = facade.get_all_reviews()
        return [{
            "id": review.id,
            "text": review.text,
            "rating": review.rating
        } for review in reviews], 200

@ns.route('/<string:review_id>')
class ReviewResource(Resource):
    @ns.response(200, 'Review details retrieved successfully')
    @ns.response(404, 'Review not found')
    def get(self, review_id):
        facade = HBnBFacade()
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return {
            "id": review.id,
            "text": review.text,
            "rating": review.rating,
            "user_id": review.user.id,
            "place_id": review.place.id
        }, 200

    @jwt_required()
    @ns.expect(update_review_model, validate=True)
    @ns.response(200, 'Review updated successfully')
    @ns.response(403, 'Unauthorized action')
    @ns.response(404, 'Review not found')
    def put(self, review_id):
        claims = get_jwt()
        facade = HBnBFacade()
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        if not claims.get('is_admin') and review.user.id != claims.get('sub'):
            return {'error': 'Unauthorized action'}, 403
        update_data = ns.payload
        try:
            updated_review = facade.update_review(review_id, update_data)
            return {"message": "Review updated successfully", "review": {
                "id": updated_review.id,
                "text": updated_review.text,
                "rating": updated_review.rating,
                "user_id": updated_review.user.id,
                "place_id": updated_review.place.id
            }}, 200
        except ValueError as e:
            return {"error": str(e)}, 400

    @jwt_required()
    @ns.response(200, 'Review deleted successfully')
    @ns.response(403, 'Unauthorized action')
    @ns.response(404, 'Review not found')
    def delete(self, review_id):
        claims = get_jwt()
        facade = HBnBFacade()
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        if not claims.get('is_admin') and review.user.id != claims.get('sub'):
            return {'error': 'Unauthorized action'}, 403
        deletion_result = facade.delete_review(review_id)
        if deletion_result:
            return {"message": "Review deleted successfully"}, 200
        else:
            return {"error": "Failed to delete review"}, 400
