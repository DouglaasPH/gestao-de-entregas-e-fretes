from src.models import Role
from src.app.app import ma

class RoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Role                     # Modelo que você quer serializar
        load_instance = True             # Permite criar objetos do modelo a partir dos dados
        include_relationships = True     # Incluir relacionamento entre
        exclude = ('user',)              # Evitar loop infinito serializando usuários