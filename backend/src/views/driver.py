from marshmallow import fields, RAISE
from src.models import Driver
from src.app.app import ma
from src.views.user import UserSchema
from src.views.driver_status import DriverStatusSchema

class CreateDriverSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        only = ('user_id', 'cnh', 'driver_status_id')
        unknown = RAISE
        
    user_id = fields.Integer(required=True)           # Mandatory
    cnh = fields.Dict(required=True)                # Mandatory
    driver_status_id = fields.Integer(required=True)  # Mandatory


class DriverSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Driver
        load_instance = True
        exclude = ('cnh_encrypted',)
    
    user_id = fields.Integer(required=True)           # Mandatory
    cnh = fields.String(required=True)                # Mandatory
    driver_status_id = fields.Integer(required=True)  # Mandatory

    user = ma.Nested(UserSchema)
    driver_status = ma.Nested(DriverStatusSchema)