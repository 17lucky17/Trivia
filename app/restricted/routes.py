# importamos la instancia de Flask (app)
from app import app, admin, db
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
# importamos los modelos a usar
from app.auth.models import User, Role
from app.public.models import Categoria, Pregunta, Respuesta
from flask import render_template, g, redirect, url_for, request, abort
from flask_login import current_user, login_required

from flask_principal import RoleNeed, UserNeed, identity_loaded, Permission

admin_permission = Permission(RoleNeed('admin'))

class MyModelView(ModelView):
    def is_accessible(self):
        has_auth = current_user.is_authenticated
        has_perm = admin_permission.allows(g.identity)
        return has_auth and has_perm

    def inaccessible_callback(self, name, **kwargs):
       return redirect(url_for('auth.login', next=request.url))

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        has_auth = current_user.is_authenticated
        has_perm = admin_permission.allows(g.identity)
        return has_auth and has_perm

    def inaccessible_callback(self, name, **kwargs):
        has_auth = current_user.is_authenticated
        has_perm = admin_permission.allows(g.identity)
        # esta loggeado pero no es admin
        if has_auth and not has_perm:
            abort(403)
        # no loggeado
        else:
            return redirect(url_for('auth.login', next=request.url))

admin.init_app(app, index_view=MyAdminIndexView())

# Los modelos que queremos mostrar en el admin
admin.add_view(MyModelView(Categoria, db.session))
admin.add_view(MyModelView(Pregunta, db.session))
admin.add_view(MyModelView(Respuesta, db.session))
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Role, db.session))

""" Flask-Principal"""
# Flask-Principal: Agregamos las necesidades a una identidad, una vez que se loguee el usuario.
# Se ejecuta cuando el usuario pasa de anónimo a estar logueado
#@identity_loaded.connect_via(app)
@identity_loaded.connect
def on_identity_loaded(sender, identity):
    # Seteamos la identidad al usuario
    identity.user = current_user

    # Agregamos una UserNeed a la identidad, con el id del usuario actual.
    if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))

    # Agregamos a la identidad la lista de roles que posee el usuario actual.
    if hasattr(current_user, 'roles'):
        for role in current_user.roles:
            identity.provides.add(RoleNeed(role.rolename))

@app.route('/admin')
@login_required
@admin_permission.require(http_exception=403)
#Este admin_permission es el creado en apptrivia.py
def mostraradmin():
    return render_template('admin.html')
