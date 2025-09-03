from app import db

place_amenity_association = db.Table(
    'Place_Amenity', db.Model.metadata,
    db.Column('place_id', db.String(36), db.ForeignKey('Place.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('Amenity.id'), primary_key=True)
)
