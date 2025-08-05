from .Base_Model import BaseModel
from app import db
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Review(BaseModel):
    """represents a Review tied to Place by Composition and dependent on User"""
    __tablename__ = 'Review'
    
    text = db.Column(db.String(500), nullable=True)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('Place.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('User.id'), nullable=False)
    user = db.relationship('User', backref='reviews', lazy=True)
    place = db.relationship('Place', backref='place_reviews', lazy=True)
    
    def __init__(self, rating, text, user=None, place=None):
        super().__init__()
        self.rating = rating
        self.text = text
        if user:
            self.user = user
            self.user_id = user.id
        if place:
            self.place = place
            self.place_id = place.id
        self.validate_review()

    def validate_review(self):
        """Validates review informations format"""

        if not isinstance(self.text, str) or not self.text.strip():
            raise ValueError("Text is required and must be a non-empty string")
        if not isinstance(self.rating, int) or not (1 <= self.rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")

    def to_dict(self):
        """Convert the review instance to a dictionary"""
        review_dict = super().to_dict()
        review_dict.update({
            'text': self.text,
            'rating': self.rating,
            'user': {
                'id': self.user.id,
                'first_name': self.user.first_name,
                'last_name': self.user.last_name,
                'email': self.user.email
            } if self.user else None,
            'place': {
                'id': self.place.id,
                'title': self.place.title,
                'description': self.place.description
            } if self.place else None
        })
        return review_dict
