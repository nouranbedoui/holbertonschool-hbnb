from .Base_Model import BaseModel
from app import db
from app.models.association_tables import place_amenity_association


class Amenity(BaseModel):
    """Represents an Amenity, Aggregated with Place"""
    __tablename__ = 'Amenity'

    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    associated_places = db.relationship('Place', secondary=place_amenity_association, backref='amenities_associated')

    def __init__(self, name, description):
        super().__init__()
        self.name = name
        self.description = description
        self.validate_amenity()

    def validate_amenity(self):
        """validates amenity informations format"""
        if not self.name or self.name.strip() == "":
            raise ValueError("name is required")

    def to_dict(self):
        """Convert the amenity instance to a dictionary"""
        amenity_dict = super().to_dict()
        amenity_dict.update({
            'name': self.name,
            'description': self.description
        })
        return amenity_dict
