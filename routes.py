# importamos la instancia de Flask (app)
from apptrivia import app
import random
import datetime
# importamos los modelos a usar
from models.models import Categoria, Pregunta, Respuesta, User
from flask import render_template, session, redirect, url_for, flash, request, jsonify
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from werkzeug.exceptions import HTTPException
from forms.register import RegisterForm
from forms.login import LoginForm


login_manager = LoginManager(app)

#con esta puedo probar si llego hasta acá -  http://localhost:5000/trivia
@app.route('/trivia')
def index():
    print(" &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& INDEX")
    session.clear()

    dicc_categorias = {"Geografía": False, "Deportes": False, "Historia": False, "Arte": False}
    session['dicc_categorias'] = dicc_categorias

    return render_template('trivia.html')

#le decimos a Flask-Login como obtener un usuario
@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))

@app.route('/trivia/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        #get by email valida
        user = User.get_by_email(form.email.data)
        if user is not None and user.check_password(form.password.data):
            # funcion provista por Flask-Login, el segundo parametro gestion el "recordar"
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next', None)
            if not next_page:
                next_page = url_for('index')
            return redirect(next_page)

        else:
            flash('Usuario o contraseña inválido')
            return redirect(url_for('login'))
    # no loggeado, dibujamos el login con el form vacio
    return render_template('login.html', form=form)

@app.route("/trivia/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
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
            # Dejamos al usuario logueado
            login_user(user, remember=True)
            return redirect(url_for('index'))
    return render_template("register.html", form=form)


@app.route('/trivia/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

""" manejo de errores """

@app.errorhandler(404)
def page_not_found(e):
    mensaje = "La página a la que desea acceder no existe"
    #return jsonify(error=str(e)), 404
    return render_template('error.html', mensaje=mensaje)
    #return render_template('404.html')


@app.errorhandler(401)
def unathorized(e):
    mensaje = "Debes estar logueado para jugar"
    #return jsonify(error=str(e)), 404
    return render_template('error.html', mensaje=mensaje)


@app.errorhandler(HTTPException)
def handle_exception(e):
    #return jsonify(error=str(e)), e.code
    mensaje = "Ha ocurrido un error inesperado. Intente nuevamente más tarde."
    return render_template('error.html', mensaje=mensaje)

@app.route('/trivia/categorias', methods=['GET'])
@login_required
def mostrarcategorias():
    categorias = Categoria.query.all()
    categs = session['dicc_categorias']
    session['hora_inicio'] = datetime.datetime.now()
    hi = session['hora_inicio']
    hora_inicio = hi.strftime("%d/%m/%Y - %H:%M:%S")
    print("Categorias en mostrarcategorias = ", session['dicc_categorias'])
    return render_template('categorias.html', categorias=categorias, inicio=hora_inicio)


@app.route('/trivia/<int:id_categoria>/pregunta', methods=['GET'])
@login_required
def mostrarpregunta(id_categoria):
    preguntas = Pregunta.query.filter_by(categoria_id=id_categoria).all()
    # elegir pregunta aleatoria pero de la categoria adecuada
    pregunta = random.choice(preguntas)
    categ = Categoria.query.get(id_categoria)

    respuestas = Respuesta.query.filter_by(pregunta_id=pregunta.id).all()

    return render_template('preguntas.html', categoria=categ, pregunta=pregunta, respuestas=respuestas)

@app.route('/trivia/<int:id_pregunta>/resultado/<int:id_respuesta>', methods=['GET'])
@login_required
def mostrarresultado(id_respuesta,id_pregunta):
    tiempo_total = 0
    minutos = 0
    segundos = 0
    tiempo_partid = ""
    hora_fin = datetime.datetime.now()
    resp = Respuesta.query.get(id_respuesta)
    preg = Pregunta.query.get(id_pregunta)
    categ = Categoria.query.get(preg.categoria_id)
    print("cats antes = ", session['dicc_categorias'])

    if resp.resultado == True:
        #categs = session['dicc_categorias']
        print("Categoria que cambio = ", categ.descripcion)
        #categs[categ.descripcion] = True
        #session['dicc_categorias'] = categs
        session['dicc_categorias'][categ.descripcion] = True
        session.modified = True

    print("cats después = ", session['dicc_categorias'])
    valores = session['dicc_categorias'].values()
    print("Valores = ", valores) #puedo ver si existe un valor en la lista?

    if False in valores:
        print("Hay falsos")
        return render_template('resultado.html', resultado=resp.resultado, pregunta=preg, respuesta=resp)
    else:
        print("NO hay falsos")
    """
    for cat in session['dicc_categorias']:
        if session['dicc_categorias'][cat] == False:
            return render_template('resultado.html', resultado="ok", pregunta=preg)
    """
    tiempo_total = hora_fin - session['hora_inicio']
    #tiempo_partida = tiempo_total.total_seconds()

    minutos = tiempo_total.total_seconds() / 60
    segundos = tiempo_total.total_seconds() % 60

    tiempo_partida = str(int(round(minutos,0))) + " minutos y " + str(int(round(segundos,0))) + " segundos"
    print("Cant minutos = ", minutos, " -- segundos = ", segundos)
    return render_template('ganador.html', tiempo=tiempo_partida, minutos=minutos)