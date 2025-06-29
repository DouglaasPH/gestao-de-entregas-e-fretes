from http import HTTPStatus

from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from sqlalchemy import inspect
from marshmallow import ValidationError

from src.models import Orders, db
from src.utils import requires_role, get_authenticated_user, can_access_user, is_self_user
from src.views.orders import CreateOrderSchema, OrderSchema, OrderUpdateSchema, OrderStatusIdUpdateSchema

app = Blueprint('orders', __name__, url_prefix='/orders')

@jwt_required()
@requires_role(['admin', 'manager', 'operator'])
def _create_order():
    orders_schema = CreateOrderSchema()
    
    try:
        data = orders_schema.load(request.json)
    except ValidationError as exc:
        return exc.messages, HTTPStatus.UNPROCESSABLE_ENTITY
    
    order = Orders(
        points_of_sale_id=data['points_of_sale_id'],
        driver_id=data['driver_id'],
        vehicle_id=data['vehicle_id'],
        weight_kg=data['weight_kg'],
        distance_km=data['distance_km'],
        load_type_id=data['load_type_id'],
        order_status_id=data['order_status_id'],
        shipping_cost=data['shipping_cost'],
        created_by=data['created_by']
    )
    db.session.add(order)
    db.session.commit()
    return { 'message': 'new order created!' }, HTTPStatus.CREATED


@jwt_required()
@requires_role(['admin', 'manager', 'operator'])
def _list_orders():
    query = db.select(Orders)
    orders = db.session.execute(query).scalars().all()
    orders_schema = OrderSchema(many=True)
    return orders_schema.dump(orders)


@app.route('/', methods=['GET', 'POST'])
def list_or_create_orders():
    if request.method == 'POST':
        return _create_order()
    else:
        return { 'orders': _list_orders() }, HTTPStatus.OK


@jwt_required()
@requires_role(['admin', 'manager', 'operator', 'driver'])
@app.route('/<int:order_id>')
def get_order(order_id):
    order = db.get_or_404(Orders, order_id)
    order_driver_user_id = order.driver.user.id
    
    if not can_access_user(order_driver_user_id):
        return { 'message': 'You do not have access.' }, HTTPStatus.FORBIDDEN
    else:
        orders_schema = OrderSchema()
        return orders_schema.dump(order)
    


@jwt_required()
@requires_role(['admin', 'manager', 'operator', 'driver'])
@app.route('/<int:order_id>', methods=['PATCH'])
def update_order(order_id):
    current_user = get_authenticated_user()
    order = db.get_or_404(Orders, order_id)
    order_driver_user_id = order.driver.user.id
    data = request.json
    
    if current_user.role.name == 'driver' and is_self_user(order_driver_user_id):
        order_schema = OrderStatusIdUpdateSchema()
        data = order_schema.load(data)
    elif current_user.role.name in ['admin', 'manager', 'operator']:
        order_schema = OrderUpdateSchema()
        data = order_schema.load(data)
    else:
        return { 'message': 'You do not have access.' }, HTTPStatus.FORBIDDEN

    for key in data:
        setattr(order, key, data[key])

    db.session.commit()
    
    return { 'message': 'Order updated.' }, HTTPStatus.OK


@jwt_required()
@requires_role(['admin'])
@app.route('/<int:order_id>', methods=['DELETE'])
def delete_user(order_id):
    order = db.get_or_404(Orders, order_id)
    db.session.delete(order)
    db.session.commit()
    
    return "", HTTPStatus.NO_CONTENT