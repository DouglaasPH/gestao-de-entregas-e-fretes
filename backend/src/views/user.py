from marshmallow import fields, RAISE
from src.models import User
from src.app.app import ma
from src.views.role import RoleSchema

class CreateUserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        only = ('name', 'cpf', 'telephone', 'email', 'password', 'role_id')  # Aceita apenas esses valores
        unknown = RAISE                                                      # Disparar erro se vier campo não permitido
        
    name = fields.String(required=True)              # Obrigatório
    cpf = fields.String(required=True)               # Obrigatório
    telephone = fields.String(required=True)         # Obrigatório
    email = fields.String(required=True)             # Obrigatório
    password = fields.String(required=True)          # Obrigatório
    role_id = fields.Integer(required=True)          # Obrigatório


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User                   # Modelo para serializar
        load_instance = True           # Permite criar objetos do modelo a partir dos dados
        include_fk = True              # Inclui chaves estrangeiras (como role_id)
        exclude = ('name_encrypted', 'cpf_encrypted', 'telephone_encrypted', 'email_encrypted', 'email_hash', 'password')         # Não retornar tabelas
    
    name = fields.String()
    cpf = fields.String()
    telephone = fields.String()
    email = fields.String()
    
    role = ma.Nested(RoleSchema, only=('id', 'name'))


class UserUpdateByAdminSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        only = ('name', 'cpf', 'telephone', 'email', 'password', 'role_id')  # Aceita apenas esses valores
        unknown = RAISE                                                      # Disparar erro se vier campo não permitido

    name = fields.String(required=False)
    cpf = fields.String(required=False)
    telephone = fields.String(required=False)
    email = fields.String(required=False)
    password = fields.String(required=False)
    role_id = fields.Integer(required=False)


class UserUpdateByOthersSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        only = ('telephone', 'email', 'password',)  # Aceita apenas esses valores
        unknown = RAISE                             # Disparar erro se vier campo não permitido

    telephone = fields.String(required=False)
    email = fields.String(required=False)
    password = fields.String(required=False)
