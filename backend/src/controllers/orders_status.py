import os
from http import HTTPStatus

from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from sqlalchemy import inspect
from marshmallow import ValidationError

from src.models import Orders_status, db
from src.utils import requires_role
from src.views.orders_status import OrdersStatusSchema, CreateOrderStatusSchema

app = Blueprint('orders_status', __name__, url_prefix='/orders_status')

@jwt_required()
@requires_role(['admin'])
def _create_orders_status():
    orders_status_schema = CreateOrderStatusSchema()
    
    try:
        data = orders_status_schema.load(request.json)
    except ValidationError as exc:
        return exc.messages, HTTPStatus.UNPROCESSABLE_ENTITY
    
    orders_status = Orders_status(
        name=data['name']
    )
    db.session.add(orders_status)
    db.session.commit()
    return { 'message': 'new order status created!' }, HTTPStatus.CREATED


@jwt_required()
@requires_role(['admin'])
def _list_orders_status():
    query = db.select(Orders_status)
    orders_status = db.session.execute(query).scalars().all()
    orders_status_schema = OrdersStatusSchema(many=True)
    return orders_status_schema.dump(orders_status)


@app.route('/', methods=['GET', 'POST'])
def list_or_create_orders_status():
    if request.method == 'POST':
        return _create_orders_status()
    else:
        return { 'orders_status': _list_orders_status() }, HTTPStatus.OK


@jwt_required()
@requires_role(['admin'])
@app.route('/<int:orders_status_id>')
def get_user(orders_status_id):
    orders_status = db.get_or_404(Orders_status, orders_status_id)
    orders_status_schema = OrdersStatusSchema()
    return orders_status_schema.dump(orders_status)


@jwt_required()
@requires_role(['admin'])
@app.route('/<int:orders_status_id>', methods=['PATCH'])
def update_orders_status(orders_status_id):
    orders_status = db.get_or_404(Orders_status, orders_status_id)
    data = request.json
    
    if 'name' in data:
        setattr(orders_status, 'name', data['name'])

    db.session.commit()
    
    return { 'message': 'order status updated.' }, HTTPStatus.OK


@jwt_required()
@requires_role(['admin'])
@app.route('/<int:orders_status_id>', methods=['DELETE'])
def delete_orders_status(orders_status_id):
    orders_status = db.get_or_404(Orders_status, orders_status_id)
    db.session.delete(orders_status)
    db.session.commit()
    
    return "", HTTPStatus.NO_CONTENT