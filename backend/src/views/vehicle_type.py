from marshmallow import fields, RAISE
from src.models import Vehicle_type
from src.app.app import ma

class CreateVehicleTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        only = ('name',)   # Aceita apenas esses valores
        unknown = RAISE    # Disparar erro se vier campo não permitido
        
    name = fields.String(required=True)           # Obrigatório


class VehicleTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Vehicle_type
        load_instance = True
    
    id = fields.Integer(required=True)       # Mandatory
    name = fields.String(required=True)      # Mandatory