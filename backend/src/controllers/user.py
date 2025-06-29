from http import HTTPStatus

from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from sqlalchemy import inspect
from marshmallow import ValidationError
import hashlib

from src.app.app import bcrypt
from src.models import User, db
from src.utils import requires_role, get_authenticated_user, get_authorized_user_or_abort, can_access_user
from src.views.user import CreateUserSchema, UserSchema, UserUpdateByAdminSchema, UserUpdateByOthersSchema


app = Blueprint('user', __name__, url_prefix='/users')

   
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


def _list_users():
    query = db.select(User)
    users = db.session.execute(query).scalars().all()
    user_schema = UserSchema(many=True)
    return user_schema.dump(users)
    

@jwt_required()
@requires_role(['admin'])
@app.route('/', methods=['GET', 'POST'])
def list_or_create_user():
    if request.method == 'POST':
        return _create_user()
    else:
        return { 'users': _list_users() }, HTTPStatus.OK


@jwt_required()
@requires_role(['admin', 'manager', 'operator', 'driver'])
@app.route('/<int:user_id_to_view>')
def get_user(user_id_to_view):
    user_schema = UserSchema()
    
    if can_access_user(user_id_to_view):
        user = db.get_or_404(User, user_id_to_view)
        return user_schema.dump(user)
    else:
        return { 'message': 'You do not have access.' }, HTTPStatus.FORBIDDEN


@jwt_required()
@requires_role(['admin', 'manager', 'operator', 'driver'])
@app.route('/<int:user_id>', methods=['PATCH'])
def update_user(user_id):
    current_user = get_authenticated_user()
    
    try:
        if current_user.role.name in ['manager', 'operator', 'driver']:
            user_schema = UserUpdateByOthersSchema()
            data = user_schema.load(request.json)
            user_to_modify = current_user
        else:
            user_schema = UserUpdateByAdminSchema()
            data = user_schema.load(request.json)
            user_to_modify = get_authorized_user_or_abort(user_id)
    except ValidationError as exc:
        return exc.messages, HTTPStatus.UNPROCESSABLE_ENTITY
    
    
    for key in data:
        if key == 'password':
            user_to_modify.password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        elif key == 'email':
            user_to_modify.email = data['email']
            user_to_modify.email_hash = hashlib.sha256(data['email'].encode()).hexdigest()
        elif key == 'role_id':
            user_to_modify.role_id = data['role_id']
        else:
            setattr(user_to_modify, key, data[key])

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