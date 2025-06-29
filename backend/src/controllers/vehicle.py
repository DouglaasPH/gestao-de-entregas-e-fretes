from http import HTTPStatus

from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from sqlalchemy import inspect
from marshmallow import ValidationError

from src.models import Vehicle, db
from src.utils import requires_role, can_access_user
from src.views.vehicle import VehicleSchema, CreateVehicleSchema, VehicleUpdateSchema

app = Blueprint('vehicle', __name__, url_prefix='/vehicle')

@jwt_required()
@requires_role(['admin'])
def _create_vehicle():
    vehicle_schema = CreateVehicleSchema()
    
    try:
        data = vehicle_schema.load(request.json)
    except ValidationError as exc:
        return exc.messages, HTTPStatus.UNPROCESSABLE_ENTITY
    
    vehicle = Vehicle(
        plate=data['plate'],
        model=data['model'],
        vehicle_type_id=data['vehicle_type_id'],
        capacity_per_kilo=data['capacity_per_kilo'],
        driver_id=data['driver_id']
    )
    db.session.add(vehicle)
    db.session.commit()
    return { 'message': 'new vehicle created!' }, HTTPStatus.CREATED


@jwt_required()
@requires_role(['admin', 'manager', 'operator'])
def _list_vehicle():
    query = db.select(Vehicle)
    vehicle = db.session.execute(query).scalars().all()
    vehicle_schema = VehicleSchema(many=True)
    return vehicle_schema.dump(vehicle)


@app.route('/', methods=['GET', 'POST'])
def list_or_create_vehicle():
    if request.method == 'POST':
        return _create_vehicle()
    else:
        return { 'vehicle': _list_vehicle() }, HTTPStatus.OK


@jwt_required()
@requires_role(['admin', 'manager', 'operator', 'driver'])
@app.route('/<int:vehicle_id>')
def get_vehicle(vehicle_id):
    vehicle = db.get_or_404(Vehicle, vehicle_id)
    driver_user_id = vehicle.driver.user.id    
    
    if not can_access_user(driver_user_id):
        return { 'message': 'You do not have access.' }, HTTPStatus.FORBIDDEN
    else:
        vehicle_schema = VehicleSchema()
        return vehicle_schema.dump(vehicle)


@jwt_required()
@requires_role(['admin', 'manager', 'operator'])
@app.route('/<int:vehicle_id>', methods=['PATCH'])
def update_vehicle(vehicle_id):
    vehicle = db.get_or_404(Vehicle, vehicle_id)
    vehicle_schema = VehicleUpdateSchema()
    data = vehicle_schema.load(request.json)
    
    for key in data:
        setattr(vehicle, key, data[key])

    db.session.commit()
    
    return { 'message': 'Vehicle updated.' }, HTTPStatus.OK


@jwt_required()
@requires_role(['admin'])
@app.route('/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    vehicle = db.get_or_404(Vehicle, vehicle_id)
    db.session.delete(vehicle)
    db.session.commit()
    
    return "", HTTPStatus.NO_CONTENT