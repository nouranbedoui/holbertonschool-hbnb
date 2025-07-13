'''Place Class'''
from datetime import datetime
from .base_model import BaseModel
from .user import User
from .amenity import Amenity


class Place(BaseModel):
    """Place class that inherits from BaseModel."""
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if len(value) > 100 or not value:
            raise ValueError("Title must be present with max 100 characters.")
        self._title = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Price must be an integer.")
        if value <= 0:
            raise ValueError("The price must be greater than 0.")
        self._price = value
        self._price = float(value)


    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, float):
            raise TypeError("Latitude must be a float.")
        if value < -90 or value > 90:
            raise ValueError("Latitude must be between -90.0 and 90.0")
        self._latitude = value

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, float):
            raise TypeError("Longitude must be a float.")
        if value < -180 or value > 180:
            raise ValueError("Longitude must be between -180.0 and 180.0")
        self._longitude = value

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, value):
        if not isinstance(value, User):
            raise TypeError("Owner must be a User instance.")
        self._owner = value

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)
        self.save()

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        if not isinstance(amenity, Amenity):
            raise TypeError("Amenity must be an Amenity instance.")
        self.amenities.append(amenity)
        self.save()

    def to_dict(self):
        """Convert the Place object to a dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner.id,
            "reviews": [review.to_dict() for review in self.reviews],
            "amenities": [amenity.to_dict() for
                          amenity in self.amenities if amenity]
        }
