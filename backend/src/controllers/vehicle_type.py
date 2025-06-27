import os
from http import HTTPStatus

from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from sqlalchemy import inspect
from marshmallow import ValidationError

from src.models import Vehicle_type, db
from src.utils import requires_role
from src.views.vehicle_type import VehicleTypeSchema, CreateVehicleTypeSchema

app = Blueprint('vehicle_type', __name__, url_prefix='/vehicle_type')

# @jwt_required()
# @requires_role(['admin'])
def _create_vehicle_type():
    vehicle_type_schema = CreateVehicleTypeSchema()
    
    try:
        data = vehicle_type_schema.load(request.json)
    except ValidationError as exc:
        return exc.messages, HTTPStatus.UNPROCESSABLE_ENTITY
    
    vehicle_type = Vehicle_type(
        name=data['name']
    )
    db.session.add(vehicle_type)
    db.session.commit()
    return { 'message': 'new vehicle type created!' }, HTTPStatus.CREATED


# @jwt_required()
# @requires_role(['admin'])
def _list_vehicle_type():
    query = db.select(Vehicle_type)
    vehicle_type = db.session.execute(query).scalars().all()
    vehicle_type_schema = VehicleTypeSchema(many=True)
    return vehicle_type_schema.dump(vehicle_type)


@app.route('/', methods=['GET', 'POST'])
def list_or_create_vehicle_type():
    if request.method == 'POST':
        return _create_vehicle_type()
    else:
        return { 'vehicle_type': _list_vehicle_type() }, HTTPStatus.OK


# @jwt_required()
# @requires_role(['admin'])
@app.route('/<int:vehicle_type_id>')
def get_user(vehicle_type_id):
    vehicle_type = db.get_or_404(Vehicle_type, vehicle_type_id)
    vehicle_type_schema = VehicleTypeSchema()
    return vehicle_type_schema.dump(vehicle_type)


# @jwt_required()
# @requires_role(['admin'])
@app.route('/<int:vehicle_type_id>', methods=['PATCH'])
def update_vehicle_type(vehicle_type_id):
    vehicle_type = db.get_or_404(Vehicle_type, vehicle_type_id)
    data = request.json
    
    if 'name' in data:
        setattr(vehicle_type, 'name', data['name'])

    db.session.commit()
    
    return { 'message': 'Vehicle Type updated.' }, HTTPStatus.OK


# @jwt_required()
# @requires_role(['admin'])
@app.route('/<int:vehicle_type_id>', methods=['DELETE'])
def delete_vehicle_type(vehicle_type_id):
    vehicle_type = db.get_or_404(Vehicle_type, vehicle_type_id)
    db.session.delete(vehicle_type)
    db.session.commit()
    
    return "", HTTPStatus.NO_CONTENT