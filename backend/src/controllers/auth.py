import hashlib
from http import HTTPStatus

from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from marshmallow import ValidationError

from src.models import User, db
from src.app.app import bcrypt
from src.views.auth import AuthSchema

app = Blueprint('auth', __name__, url_prefix='/auth')

def _valid_email_hashlib(email):
    return hashlib.sha256(email.encode()).hexdigest()

def _valid_password(password_hash, password_raw):
    return bcrypt.check_password_hash(password_hash, password_raw)

@app.route('/login', methods=['POST'])
def login():
    auth_schema = AuthSchema()
    
    try:
        data = auth_schema.load(request.json)
    except ValidationError as exc:
        return exc.messages, HTTPStatus.UNPROCESSABLE_ENTITY
        
    email_hash_imput = _valid_email_hashlib(data['email'])
    
    user = db.session.execute(db.select(User).where(User.email_hash == email_hash_imput)).scalar()
    
    if not user or not _valid_password(user.password, data['password']):
        return { 'message': 'Bad username or password' }, HTTPStatus.UNAUTHORIZED

    access_token = create_access_token(identity=str(user.id))
    return { 'access_token': access_token }