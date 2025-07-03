from projeto import database, app
from projeto.models import Usuario, Categoria, Tarefas

with app.app_context():
    database.create_all()
    print("Banco de dados criado com sucesso!")
