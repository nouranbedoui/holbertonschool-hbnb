'''Review Class'''


from .base_model import BaseModel
from .user import User
from .place import Place


class Review(BaseModel):
    def __init__(self, text, user_id, place_id, rating):
        super().__init__()
        self._user_id = user_id
        self._place_id = place_id
        self.text = text
        self.rating = rating

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, string):
        if not string or len(string) > 500:
            raise ValueError(
                "Text review must be present and with 500 characters maximum."
            )
        self._text = string

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        if not isinstance(value, User):
            raise ValueError("User must be present and an instance of User.")
        self._user_id = value

    @property
    def place_id(self):
        return self._place_id

    @place_id.setter
    def place_id(self, value):
        if not isinstance(value, Place):
            raise ValueError("Place must be present and an instance of Place.")
        self._place_id = value

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        if value < 1 or value > 5:
            raise ValueError("Rating must be between 1 and 5.")
        if not isinstance(value, int):
            raise TypeError("Rating must be an integer.")
        self._rating = value

    def to_dict(self):
        '''Convert the Review object to a dictionary'''
        return {
            'id': self.id,
            'text': self._text,
            'user_id': self._user_id,
            'place_id': self._place_id,
            'rating': self._rating
        }
