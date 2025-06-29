from marshmallow import fields, RAISE
from src.app.app import ma

class AuthSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        only = ('email', 'password')   # Aceita apenas esses valores
        unknown = RAISE                # Disparar erro se vier campo não permitido
        
    email = fields.String(required=True)           # Obrigatório
    password = fields.String(required=True)           # Obrigatório