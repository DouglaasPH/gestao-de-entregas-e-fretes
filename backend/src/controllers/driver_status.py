import os
from http import HTTPStatus

from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from sqlalchemy import inspect
from marshmallow import ValidationError

from src.models import Driver_status, db
from src.utils import requires_role
from src.views.driver_status import DriverStatusSchema, CreateDriverStatusSchema

app = Blueprint('driver_status', __name__, url_prefix='/driver_status')

@jwt_required()
@requires_role(['admin'])
def _create_driver_status():
    driver_status_schema = CreateDriverStatusSchema()
    
    try:
        data = driver_status_schema.load(request.json)
    except ValidationError as exc:
        return exc.messages, HTTPStatus.UNPROCESSABLE_ENTITY
    
    driver_status = Driver_status(
        name=data['name']
    )
    db.session.add(driver_status)
    db.session.commit()
    return { 'message': 'new driver status created!' }, HTTPStatus.CREATED


@jwt_required()
@requires_role(['admin'])
def _list_driver_status():
    query = db.select(Driver_status)
    driver_status = db.session.execute(query).scalars().all()
    driver_status_schema = DriverStatusSchema(many=True)
    return driver_status_schema.dump(driver_status)


@app.route('/', methods=['GET', 'POST'])
def list_or_create_drive_status():
    if request.method == 'POST':
        return _create_driver_status()
    else:
        return { 'driver_status': _list_driver_status() }, HTTPStatus.OK


@jwt_required()
@requires_role(['admin'])
@app.route('/<int:driver_status_id>')
def get_user(driver_status_id):
    driver_status = db.get_or_404(Driver_status, driver_status_id)
    driver_status_schema = DriverStatusSchema()
    return driver_status_schema.dump(driver_status)


@jwt_required()
@requires_role(['admin'])
@app.route('/<int:driver_status_id>', methods=['PATCH'])
def update_driver_status(driver_status_id):
    driver_status = db.get_or_404(Driver_status, driver_status_id)
    data = request.json
    
    if 'name' in data:
        setattr(driver_status, 'name', data['name'])

    db.session.commit()
    
    return { 'message': 'Driver status updated.' }, HTTPStatus.OK


@jwt_required()
@requires_role(['admin'])
@app.route('/<int:driver_status_id>', methods=['DELETE'])
def delete_drive_status(driver_status_id):
    driver_status = db.get_or_404(Driver_status, driver_status_id)
    db.session.delete(driver_status)
    db.session.commit()
    
    return "", HTTPStatus.NO_CONTENT