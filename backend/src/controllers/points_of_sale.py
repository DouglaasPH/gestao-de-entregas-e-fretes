import os
from http import HTTPStatus

from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from sqlalchemy import inspect
from marshmallow import ValidationError

from src.models import Points_of_sale, db
from src.utils import requires_role
from src.views.points_of_sale import CreatePointOfSaleSchema, PointOfSaleSchema

app = Blueprint('point_of_sale', __name__, url_prefix='/points_of_sale')

@jwt_required()
@requires_role(['admin', 'manager'])
def _create_point_of_sale():
    point_of_sale_schema = CreatePointOfSaleSchema()
    
    try:
        data = point_of_sale_schema.load(request.json)
    except ValidationError as exc:
        return exc.messages, HTTPStatus.UNPROCESSABLE_ENTITY
    
    point_of_sale = Points_of_sale(
        cnpj= data['cnpj'],
        telephone= data['telephone'],
        address= data['address'],
    )
    db.session.add(point_of_sale)
    db.session.commit()
    return { 'message': 'Point of sale created!' }, HTTPStatus.CREATED


@jwt_required()
@requires_role(['admin', 'manager', 'operator'])
def _list_points_of_sale():
    query = db.select(Points_of_sale)
    points_of_sale = db.session.execute(query).scalars().all()
    point_of_sale_schema = PointOfSaleSchema(many=True)
    return point_of_sale_schema.dump(points_of_sale)
    

@app.route('/', methods=['GET', 'POST'])
def list_or_create_point_of_sale():
    if request.method == 'POST':
        return _create_point_of_sale()
    else:
        return { 'points_of_sale': _list_points_of_sale() }, HTTPStatus.OK


@jwt_required()
@requires_role(['admin', 'manager', 'operator'])
@app.route('/<int:point_of_sale_id>')
def get_point_of_sale(point_of_sale_id):
    points_of_sale = db.get_or_404(Points_of_sale, point_of_sale_id)
    points_of_sale_schema = PointOfSaleSchema()
    return points_of_sale_schema.dump(points_of_sale)


@jwt_required()
@requires_role(['admin', 'manager'])
@app.route('/<int:point_of_sale_id>', methods=['PATCH'])
def update_point_of_sale(point_of_sale_id):
    point_of_sale = db.get_or_404(Points_of_sale, point_of_sale_id)
    data = request.json
    
    for key in ['cnpj', 'telephone', 'address']:
        if key in data:
            setattr(point_of_sale, key, data[key])

    db.session.commit()
    
    return { 'message': 'Point of sale updated.' }, HTTPStatus.OK


@jwt_required()
@requires_role(['admin'])
@app.route('/<int:point_of_sale_id>', methods=['DELETE'])
def delete_point_of_sale(point_of_sale_id):
    point_of_sale = db.get_or_404(Points_of_sale, point_of_sale_id)
    db.session.delete(point_of_sale)
    db.session.commit()
    
    return "", HTTPStatus.NO_CONTENT