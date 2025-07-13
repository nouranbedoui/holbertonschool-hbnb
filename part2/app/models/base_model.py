'''Base Model module.
This module defines a base class for other models,
providing unique ID generation and timestamp management.
'''


import uuid
from datetime import datetime


class BaseModel:
    '''Represents a base model with id and timestamp attributes'''
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        '''Update the `updated_at` timestamp to the current time.'''
        self.updated_at = datetime.now()

    def update(self, data):
        '''Update instance attributes based on the given dictionary : data'''
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
