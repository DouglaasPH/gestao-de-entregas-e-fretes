from marshmallow import fields, RAISE
from src.models import Orders_status
from src.app.app import ma

class CreateOrderStatusSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        only = ('name',)
        unknown = RAISE
        
    name = fields.String(required=True)           # Mandatory


class OrdersStatusSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Orders_status
        load_instance = True
    
    id = fields.Integer(required=True)            # Mandatory
    name = fields.String(required=True)           # Mandatory