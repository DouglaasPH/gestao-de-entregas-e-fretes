from marshmallow import fields, RAISE
from src.models import Orders
from src.app.app import ma
from src.views.points_of_sale import PointOfSaleSchema
from src.views.driver import DriverSchema
from src.views.vehicle import VehicleSchema
from src.views.load_type import LoadTypeSchema
from backend.src.views.orders_status import OrdersStatusSchema
from backend.src.views.user import UserSchema

class CreateOrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        only = ('points_of_sale_id', 'driver_id', 'vehicle_id', 'weight_kg', 'distance_km', 'load_type_id', 'order_status_id', 'shipping_cost', 'created_by')
        unknown = RAISE
        
    points_of_sale_id = fields.Integer(required=True)      # Obrigatório
    driver_id = fields.Integer(required=True)              # Obrigatório
    vehicle_id = fields.Integer(required=True)             # Obrigatório
    weight_kg = fields.Integer(required=True)              # Obrigatório
    distance_km = fields.Integer(required=True)            # Obrigatório
    load_type_id = fields.Integer(required=True)           # Obrigatório
    order_status_id = fields.Integer(required=True)        # Obrigatório
    shipping_cost = fields.Integer(required=True)          # Obrigatório
    created_by = fields.Integer(required=True)             # Obrigatório
    

class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Orders                   # Modelo para serializar
        load_instance = True           # Permite criar objetos do modelo a partir dos dados
        include_fk = True              # Inclui chaves estrangeiras
        exclude = ('points_of_sale_id', 'driver_id', 'vehicle_id', 'load_type_id', 'order_status_id', 'created_by')         # Não retornar tabelas
    
    point_of_sale = ma.Nested(PointOfSaleSchema)
    driver = ma.Nested(DriverSchema)
    vehicle = ma.Nested(VehicleSchema)
    load_type = ma.Nested(LoadTypeSchema)
    order_status = ma.Nested(OrdersStatusSchema)
    created_by = ma.Nested(UserSchema)


class OrderUpdateSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        only = ('points_of_sale_id', 'driver_id', 'vehicle_id', 'weight_kg', 'distance_km', 'load_type_id', 'order_status_id', 'shipping_cost', 'created_by')
        unknown = RAISE
        
    points_of_sale_id = fields.Integer(required=False)
    driver_id = fields.Integer(required=False)
    vehicle_id = fields.Integer(required=False)
    weight_kg = fields.Integer(required=False)
    distance_km = fields.Integer(required=False)
    load_type_id = fields.Integer(required=False)
    order_status_id = fields.Integer(required=False)
    shipping_cost = fields.Integer(required=False)
    created_by = fields.Integer(required=False)


class OrderStatusIdUpdateSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        only = ('order_status_id',)
        unknown = RAISE
        
    order_status_id = fields.Integer(required=True)