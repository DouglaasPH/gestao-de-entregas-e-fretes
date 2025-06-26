import os
from http import HTTPStatus

from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from sqlalchemy import inspect
from marshmallow import ValidationError
import hashlib

from src.app.app import bcrypt
from src.models import User, db
from src.utils import requires_role
from src.views.user import CreateUserSchema, UserSchema


app = Blueprint('user', __name__, url_prefix='/users')

@jwt_required()
@requires_role(['admin'])
def _create_user():
    user_schema = CreateUserSchema()
    
    try:
        data = user_schema.load(request.json)
    except ValidationError as exc:
        return exc.messages, HTTPStatus.UNPROCESSABLE_ENTITY
    
    user = User(
        name= data['name'],
        cpf= data['cpf'],
        telephone= data['telephone'],
        email= data['email'],
        email_hash= hashlib.sha256(data['email'].encode()).hexdigest(),
        password= bcrypt.generate_password_hash(data['password']).decode('utf-8'),
        role_id= data['role_id'],
    )
    db.session.add(user)
    db.session.commit()
    return { 'message': 'User created!' }, HTTPStatus.CREATED


# @jwt_required()
# @requires_role(['admin'])
def _list_users():
    query = db.select(User)
    users = db.session.execute(query).scalars().all()
    user_schema = UserSchema(many=True)
    return user_schema.dump(users)
    

@app.route('/', methods=['GET', 'POST'])
def list_or_create_user():
    if request.method == 'POST':
        return _create_user()
    else:
        return { 'users': _list_users() }, HTTPStatus.OK


@jwt_required()
@requires_role(['admin'])
@app.route('/<int:user_id>')
def get_user(user_id):
    user = db.get_or_404(User, user_id)
    user_schema = UserSchema()
    return user_schema.dump(user)


@jwt_required()
@requires_role(['admin'])
@app.route('/<int:user_id>', methods=['PATCH'])
def update_user(user_id):
    user = db.get_or_404(User, user_id)
    data = request.json
    
    for key in ['name', 'cpf', 'telephone', 'email']:
        if key in data:
            setattr(user, key, data[key])
            if key == 'email':
                user.email_hash = hashlib.sha256(data['email'].encode()).hexdigest()

    if 'password' in data:
        user.password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    if 'role_id' in data:
        user.role_id = data['role_id']
    
    db.session.commit()
    
    return { 'message': 'User updated.' }, HTTPStatus.OK


@jwt_required()
@requires_role(['admin'])
@app.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()
    
    return "", HTTPStatus.NO_CONTENT