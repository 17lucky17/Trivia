from flask import Flask, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

# instancia Flask
app = Flask(__name__)
admin = Admin(app)

# inicializa la base de datos con la config leida
db = SQLAlchemy(app)

# lee la config desde el archivo config.py
app.config.from_pyfile('config.py')


# rutas disponibles
from routes import *
from models.models import Categoria, Pregunta, Usuario, Respuesta

# Los modelos que queremos mostrar en el admin
admin.add_view(ModelView(Categoria, db.session))
admin.add_view(ModelView(Pregunta, db.session))
admin.add_view(ModelView(Respuesta, db.session))

#Agrego el modelo Usuario al Flask Admin
admin.add_view(ModelView(Usuario, db.session))

# subimos el server (solo cuando se llama directamente a este archivo)
if __name__ == '__main__':
    app.run()