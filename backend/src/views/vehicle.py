from marshmallow import fields, RAISE
from src.models import Vehicle
from src.app.app import ma
from src.views.vehicle_type import VehicleTypeSchema
from src.views.driver import DriverSchema

class CreateVehicleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        only = ('plate', 'model', 'vehicle_type_id', 'capacity', 'driver_id')
        unknown = RAISE
        
    plate = fields.String(required=True)                  # Mandatory
    model = fields.String(required=True)                  # Mandatory
    vehicle_type_id = fields.Integer(required=True)       # Mandatory
    capacity = fields.String(required=True)               # Mandatory
    driver_id = fields.Integer(required=True)             # Mandatory


class VehicleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Vehicle
        load_instance = True
        exclude = ('plate_encrypted',)
    
    plate = fields.String(required=True)                  # Mandatory
    model = fields.String(required=True)                  # Mandatory
    vehicle_type_id = fields.Integer(required=True)       # Mandatory
    capacity = fields.String(required=True)               # Mandatory
    driver_id = fields.Integer(required=True)             # Mandatory

    vehicle_type = ma.Nested(VehicleTypeSchema)
    driver = ma.Nested(DriverSchema)