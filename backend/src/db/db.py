import sqlite3
import click

from flask import current_app, g

def get_db():
    """
    Cria uma conexão com o banco de dados SQLite.

    - Se já existir uma conexão no objeto 'g' (contexto da aplicação), reutiliza.
    - Caso contrário, cria uma nova conexão usando o caminho definido na configuração 'DATABASE'.
    - Define 'row_factory' para acessar os resultados como dicionários (row["coluna"]).

    Returns:
        sqlite3.Connection: Conexão ativa com o banco de dados.
    """
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'], # Caminho do banco configurado no app
            detect_types=sqlite3.PARSE_DECLTYPES # Permite reconhecer tipos declarados no SQL
            )
        g.db.row_factory = sqlite3.Row # Permite acesso aos dados por nome da coluna

    return g.db


def close_db(e=None):
    """
    Fecha a conexão com o banco de dados, se existir.

    - Remove a conexão do objeto 'g' e a fecha.
    - Essa função é chamada automaticamente ao encerrar o contexto da aplicação.
    
    Args:
        e (Exception, optional): Erro, se houver, passado automaticamente pelo Flask.
    """
    db = g.pop('db', None)
    
    if db is not None:
        db.close()


def init_db():
    """
    Inicializa o banco de dados.

    - Abre o arquivo 'schema.sql' que contém os comandos SQL para criação das tabelas.
    - Executa o script SQL no banco de dados atual.
    """
    db = get_db()
    
    with current_app.open_resource("../db/schema.sql") as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    """
    Comando de terminal para inicializar o banco de dados.

    - Executa a função init_db().
    - Mostra uma mensagem no terminal confirmando a inicialização.
    """
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    """
    Registra funções no app Flask.

    - Adiciona a função close_db() para ser executada automaticamente 
      quando o contexto da aplicação terminar (fim da requisição).
    - Adiciona o comando init-db na CLI do Flask para criar o banco.

    Args:
        app (Flask): Instância do aplicativo Flask.
    """
    app.teardown_appcontext(close_db) # Fecha o banco após cada requisição
    app.cli.add_command(init_db_command) # Adiciona o comando flask init-db na CLI