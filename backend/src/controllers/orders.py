import os
from http import HTTPStatus

from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from sqlalchemy import inspect
from marshmallow import ValidationError

from src.models import Orders, db
from src.utils import requires_role
from src.views.orders import CreateOrderSchema, OrderSchema

app = Blueprint('orders', __name__, url_prefix='/orders')

# @jwt_required()
# @requires_role(['admin'])
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


# @jwt_required()
# @requires_role(['admin'])
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


# @jwt_required()
# @requires_role(['admin'])
@app.route('/<int:order_id>')
def get_order(order_id):
    order = db.get_or_404(Orders, order_id)
    orders_schema = OrderSchema()
    return orders_schema.dump(order)


# @jwt_required()
# @requires_role(['admin'])
@app.route('/<int:order_id>', methods=['PATCH'])
def update_order(order_id):
    order = db.get_or_404(Orders, order_id)
    data = request.json
    
    for key in ['points_of_sale_id', 'driver_id', 'vehicle_id', 'weight_kg', 'distance_km', 'load_type_id', 'order_status_id', 'shipping_cost', 'created_by']:
        if key in data:
            setattr(order, key, data[key])

    db.session.commit()
    
    return { 'message': 'Order updated.' }, HTTPStatus.OK


# @jwt_required()
# @requires_role(['admin'])
@app.route('/<int:order_id>', methods=['DELETE'])
def delete_user(order_id):
    order = db.get_or_404(Orders, order_id)
    db.session.delete(order)
    db.session.commit()
    
    return "", HTTPStatus.NO_CONTENT