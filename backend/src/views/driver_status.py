from marshmallow import fields, RAISE
from src.models import Driver_status
from src.app.app import ma

class CreateDriverStatusSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        only = ('name',)   # Aceita apenas esses valores
        unknown = RAISE    # Disparar erro se vier campo não permitido
        
    name = fields.String(required=True)           # Obrigatório


class DriverStatusSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Driver_status
        load_instance = True
    
    id = fields.Integer(required=True)       # Mandatory
    name = fields.String(required=True)      # Mandatory