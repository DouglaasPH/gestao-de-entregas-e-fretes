import os
from http import HTTPStatus

from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from sqlalchemy import inspect
from marshmallow import ValidationError

from src.models import Driver, db
from src.utils import requires_role, get_authenticated_user, can_access_driver, is_self_user
from src.views.driver import CreateDriverSchema, DriverSchema, UpdateDriverStatusSchema, UpdateDriverSchema

app = Blueprint('driver', __name__, url_prefix='/driver')

@jwt_required()
@requires_role(['admin', 'manager'])
def _create_driver():
    driver_schema = CreateDriverSchema()
    
    try:
        data = driver_schema.load(request.json)
    except ValidationError as exc:
        return exc.messages, HTTPStatus.UNPROCESSABLE_ENTITY
    
    driver = Driver(
        user_id=data['user_id'],
        cnh=data['cnh'],
        driver_status_id=data['driver_status_id'],
    )
    db.session.add(driver)
    db.session.commit()
    return { 'message': 'new driver created!' }, HTTPStatus.CREATED


@jwt_required()
@requires_role(['admin', 'manager', 'operator'])
def _list_driver():
    query = db.select(Driver)
    driver = db.session.execute(query).scalars().all()
    driver_schema = DriverSchema(many=True)
    return driver_schema.dump(driver)


@app.route('/', methods=['GET', 'POST'])
def list_or_create_drive():
    if request.method == 'POST':
        return _create_driver()
    else:
        return { 'driver': _list_driver() }, HTTPStatus.OK


@jwt_required()
@requires_role(['admin', 'manager', 'operator', 'driver'])
@app.route('/<int:driver_id>')
def get_user(driver_id):
    driver = db.get_or_404(Driver, driver_id)
    driver_user_id = driver.user.id
    
    if not can_access_driver(driver_user_id):
        return { 'message': 'You do not have access.' }, HTTPStatus.FORBIDDEN
    else:
        driver_schema = DriverSchema()
        return driver_schema.dump(driver)


@jwt_required()
@requires_role(['admin', 'manager', 'operator', 'driver'])
@app.route('/<int:driver_id>', methods=['PATCH'])
def update_driver(driver_id):
    current_user = get_authenticated_user()
    driver = db.get_or_404(Driver, driver_id)
    driver_user_id = driver.user.id
    
    try:
        if current_user.role.name in ['admin', 'manager', 'operator']:
            driver_schema = UpdateDriverSchema()
            data = driver_schema.load(request.json)
        elif current_user.role.name in ['driver'] and is_self_user(driver_user_id):
            driver_schema = UpdateDriverStatusSchema()
            data = driver_schema.load(request.json)
        else:
            return { 'message': 'You do not have access.' }, HTTPStatus.FORBIDDEN
    except ValidationError as exc:
        return exc.messages, HTTPStatus.UNPROCESSABLE_ENTITY
    
    for key in data:
        setattr(driver, key, data[key])

    db.session.commit()
    
    return { 'message': 'Driver updated.' }, HTTPStatus.OK


@jwt_required()
@requires_role(['admin', 'manager'])
@app.route('/<int:driver_id>', methods=['DELETE'])
def delete_user(driver_id):
    driver = db.get_or_404(Driver, driver_id)
    db.session.delete(driver)
    db.session.commit()
    
    return "", HTTPStatus.NO_CONTENT