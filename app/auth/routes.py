# importamos la instancia de Flask (app)
from app import app, login_manager
from . import auth_bp
# importamos los modelos a usar
from app.auth.models import User, Role
from flask import render_template, session, redirect, url_for, flash, request, jsonify
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from .forms.register import RegisterForm
from .forms.login import LoginForm
from flask_principal import AnonymousIdentity, RoleNeed, UserNeed, identity_loaded, identity_changed

#le decimos a Flask-Login como obtener un usuario
@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))

@auth_bp.route('/trivia/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))
    form = LoginForm()
    if form.validate_on_submit():
        #print("mail = ", form.email.data)
        #get by email valida
        user = User.get_by_email(form.email.data)
        if user is not None and user.check_password(form.password.data):
            # funcion provista por Flask-Login, el segundo parametro gestion el "recordar"
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next', None)
            if not next_page:
                next_page = url_for('public.index')
            return redirect(next_page)

        else:
            flash('Usuario o contraseña inválido')
            return redirect(url_for('auth.login'))
    # no loggeado, dibujamos el login con el form vacio
    return render_template('login.html', form=form)

@auth_bp.route("/trivia/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))
    form = RegisterForm()
    error = None
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        # Comprobamos que no hay ya un usuario con ese email
        user = User.get_by_email(email)
        if user is not None:
            flash('El email {} ya está siendo utilizado por otro usuario'.format(email))
        else:
            # Creamos el usuario y lo guardamos
            user = User(name=username, email=email)
            user.set_password(password)
            user.save()
            # Creo el rol del nuevo usuaricio
            usuario_nuevo = User.get_by_email(email)
            rol = Role(rolename="user", user_id=usuario_nuevo.id)
            rol.save()
            # Dejamos al usuario logueado
            login_user(user, remember=True)
            return redirect(url_for('public.index'))
    return render_template("register.html", form=form)

@auth_bp.route('/trivia/logout')
def logout():
    logout_user()
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    # Flask-Principal: the user is now anonymous
    identity_changed.send(app, identity=AnonymousIdentity())
    return redirect(url_for('public.index'))
