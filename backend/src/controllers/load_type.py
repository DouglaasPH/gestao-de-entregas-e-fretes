import os
from http import HTTPStatus

from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from sqlalchemy import inspect
from marshmallow import ValidationError

from src.models import Load_type, db
from src.utils import requires_role
from src.views.load_type import LoadTypeSchema, CreateLoadTypeSchema

app = Blueprint('load_type', __name__, url_prefix='/load_type')

# @jwt_required()
# @requires_role(['admin'])
def _create_load_type():
    load_type_schema = CreateLoadTypeSchema()
    
    try:
        data = load_type_schema.load(request.json)
    except ValidationError as exc:
        return exc.messages, HTTPStatus.UNPROCESSABLE_ENTITY
    
    load_type = Load_type(
        name=data['name']
    )
    db.session.add(load_type)
    db.session.commit()
    return { 'message': 'new load type created!' }, HTTPStatus.CREATED


# @jwt_required()
# @requires_role(['admin'])
def _list_load_type():
    query = db.select(Load_type)
    load_type = db.session.execute(query).scalars().all()
    load_type_schema = LoadTypeSchema(many=True)
    return load_type_schema.dump(load_type)


@app.route('/', methods=['GET', 'POST'])
def list_or_create_load_type():
    if request.method == 'POST':
        return _create_load_type()
    else:
        return { 'load_type': _list_load_type() }, HTTPStatus.OK


# @jwt_required()
# @requires_role(['admin'])
@app.route('/<int:load_type_id>')
def get_load_type_by_id(load_type_id):
    load_type = db.get_or_404(Load_type, load_type_id)
    load_type_schema = LoadTypeSchema()
    return load_type_schema.dump(load_type)


# @jwt_required()
# @requires_role(['admin'])
@app.route('/<int:load_type_id>', methods=['PATCH'])
def update_load_type(load_type_id):
    load_type = db.get_or_404(Load_type, load_type_id)
    data = request.json
    
    if 'name' in data:
        setattr(load_type, 'name', data['name'])

    db.session.commit()
    
    return { 'message': 'Load type updated.' }, HTTPStatus.OK


# @jwt_required()
# @requires_role(['admin'])
@app.route('/<int:load_type_id>', methods=['DELETE'])
def delete_load_type(load_type_id):
    load_type = db.get_or_404(Load_type, load_type_id)
    db.session.delete(load_type)
    db.session.commit()
    
    return "", HTTPStatus.NO_CONTENT