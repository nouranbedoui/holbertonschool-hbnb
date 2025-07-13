from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class HBnBFacade:
    """Facade for managing users, places, amenities, and reviews."""

    def __init__(self):
        """Initialize repositories for different models."""
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # User Facade
    def create_user(self, user_data):
        """Create a new user with validation."""
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Retrieve a user by ID."""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Retrieve a user by email."""
        return self.user_repo.get_by_attribute('email', email)

    def update_user(self, user_id, user_data):
        """Update user details with validation."""
        user = self.get_user(user_id)
        if not user:
            raise ValueError("User not found")
        user.update(user_data)
        self.user_repo.save(user)
        return user

    def get_all_users(self):
        """Retrieve all users."""
        return self.user_repo.get_all()

    # Amenity Facade
    def create_amenity(self, amenity_data):
        """Create a new amenity."""
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Retrieve an amenity by ID."""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Retrieve all amenities."""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update an amenity."""
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found")

        amenity.update(amenity_data)
        self.amenity_repo.save(amenity)
        return amenity

    def get_amenity_by_name(self, name):
        """Retrieve an amenity by name."""
        return self.amenity_repo.get_by_attribute('name', name)

    # Place Facade
    def create_place(self, title, description, price, latitude,
                     longitude, owner_id, amenities=None):
        """Create a new place with validation."""
        owner = self.get_user(owner_id)

        if not owner:
            raise ValueError("Owner not found.")
        if price <= 0:
            raise ValueError("Price must be a positive number.")
        if not (-90 <= latitude <= 90) or not isinstance(latitude, float):
            raise ValueError("Latitude must be between -90.0 and 90.0")
        if not (-180 <= longitude <= 180) or not isinstance(longitude, float):
            raise ValueError("Longitude must be between -180.0 and 180.0")

        place = Place(
            title=title,
            description=description,
            price=price,
            latitude=latitude,
            longitude=longitude,
            owner=owner
        )

        if amenities:
            for amenity_id in amenities:
                amenity = self.get_amenity(amenity_id)
                if not amenity:
                    raise ValueError(
                        f"Amenity with ID {amenity_id} not found."
                    )
                place.add_amenity(amenity)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """Retrieve a place by ID."""
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")
        return place

    def get_all_places(self):
        """Retrieve all places."""
        return self.place_repo.get_all()
    
    
    def update_place(self, place_id, place_data):
        """the function will update a place with new data"""
        place = self.place_repo.get(place_id)
       
        if not place:
            raise KeyError("Place not found")

        if 'title' in place_data and len(place_data['title']) > 100 \
                or not place_data['title']:
            raise ValueError("Title is required with max 100 characters.")

        if 'description' in place_data and \
                len(place_data['description']) > 1000:
            raise ValueError("Description must be less than 1000 characters.")

        if ('price' in place_data and place_data['price'] <= 0):
            raise ValueError("Price must be greater than 0.")

        if 'latitude' in place_data and \
                not (90.0 >= place_data['latitude'] >= -90.0) \
                    or not isinstance(place_data['latitude'], float):
            raise ValueError("Latitude must be between 90 and -90.")

        if 'longitude' in place_data and \
                not (180.0 >= place_data['longitude'] >= -180.0) \
                    or not isinstance(place_data['longitude'], float):
            raise ValueError("Longitude must be between 180 and -180.")

        if 'owner_id' in place_data and \
                not self.user_repo.get(place_data['owner_id']):
            raise ValueError("Owner not found, please enter a valid owner")

        if 'amenities' in place_data:
            amenities = []
            for amenity_id in place_data['amenities']:
                amenity = self.get_amenity(amenity_id)
                if not amenity:
                    raise ValueError(f"Amenity with ID {amenity_id} not found.")
                amenities.append(amenity)
            place.amenities = amenities

        for key, value in place_data.items():
            if hasattr(place, key) and key != 'amenities':
                setattr(place, key, value)

        self.place_repo.save(place)
        return place

    # Review Facade
    def create_review(self, text, user_id, place_id, rating):
        """Create a new review."""
        user = self.get_user(user_id)
        if not user:
            raise ValueError("User not found.")

        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found.")

        review = Review(
            text=text,
            user_id=user.id,
            place_id=place.id,
            rating=rating,
        )
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found")
        return review

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")
        return [review for review in
                self.review_repo.get_all() if review.place_id == place_id]

    def update_review(self, review_id, review_update):
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found")
        for key, value in review_update.items():
            if hasattr(review, key):
                setattr(review, key, value)
        self.review_repo.update(review_id, review.__dict__)
        return review

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found")
        self.review_repo.delete(review_id)
        return {'message': 'Review deleted succesessfully'}
