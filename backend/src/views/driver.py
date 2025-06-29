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
        exclude = ('cnh_encrypted', 'driver_status_id')
    
    user_id = fields.Integer(required=True)           # Mandatory
    cnh = fields.String(required=True)                # Mandatory
    driver_status_id = fields.Integer(required=True)  # Mandatory

    user = ma.Nested(UserSchema)
    driver_status = ma.Nested(DriverStatusSchema)


class UpdateDriverStatusSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        only = ('driver_status_id',)  # Aceita apenas esses valores
        unknown = RAISE               # Disparar erro se vier campo não permitido

    driver_status_id = fields.String(required=True)


class UpdateDriverSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        only = ('user_id', 'cnh', 'driver_status_id')
        unknown = RAISE
        
    user_id = fields.Integer(required=False)                # Mandatory
    cnh = fields.Dict(required=False)                       # Mandatory
    driver_status_id = fields.Integer(required=False)       # Mandatory