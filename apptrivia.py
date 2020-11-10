from flask import Flask, session, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
import os

# instancia Flask
app = Flask(__name__)

# sesiones
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or \
    'e5ac358c-f0bf-11e5-9e39-d3b532c10a28'

# inicializa la base de datos con la config leida
db = SQLAlchemy(app)

# lee la config desde el archivo config.py
app.config.from_pyfile('config.py')

class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

admin = Admin(app, index_view=MyAdminIndexView())

# rutas disponibles
from routes import *
from models.models import Categoria, Pregunta, User, Respuesta
from flask_login import LoginManager, current_user

# Los modelos que queremos mostrar en el admin
admin.add_view(MyModelView(Categoria, db.session))
admin.add_view(MyModelView(Pregunta, db.session))
admin.add_view(MyModelView(Respuesta, db.session))
admin.add_view(MyModelView(User, db.session))


# subimos el server (solo cuando se llama directamente a este archivo)
if __name__ == '__main__':
    app.run()