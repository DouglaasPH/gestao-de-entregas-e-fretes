from marshmallow import fields, RAISE
from src.models import Points_of_sale
from src.app.app import ma
from src.views.role import RoleSchema

class CreatePointOfSaleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        only = ('cnpj', 'telephone', 'address')   # Aceita apenas esses valores
        unknown = RAISE                           # Disparar erro se vier campo não permitido
        
    cnpj = fields.String(required=True)           # Obrigatório
    telephone = fields.String(required=True)      # Obrigatório
    address = fields.String(required=True)        # Obrigatório


class PointOfSaleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Points_of_sale         # Modelo para serializar
        load_instance = True           # Permite criar objetos do modelo a partir dos dados
        exclude = ('cnpj_encrypted', 'telephone_encrypted', 'address_encrypted')         # Não retornar tabelas
        
    cnpj = fields.String(required=True)           # Obrigatório
    telephone = fields.String(required=True)      # Obrigatório
    address = fields.String(required=True)        # Obrigatório