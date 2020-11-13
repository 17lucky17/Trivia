# importamos la instancia de Flask (app)
import random
import datetime
from . import public_bp
# importamos los modelos a usar
from .models import Categoria, Pregunta, Respuesta
from app.auth.models import User
from flask import render_template, session
from flask_login import current_user
from app import login_required

from ..restricted.routes import admin_permission

#con esta puedo probar si llego hasta acá -  http://localhost:5000/trivia
@public_bp.route('/trivia')
def index():
    print(" &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& INDEX")
    #session.clear()
    dicc_categorias = {"Geografía":False, "Deportes":False, "Historia":False, "Arte":False, "Cine":False, "Ciencia":False}
    session['dicc_categorias'] = dicc_categorias
    session['hora_inicio'] = None

    return render_template('trivia.html')

@public_bp.route('/trivia/categorias', methods=['GET'])
@login_required
def mostrarcategorias():
    categorias = Categoria.query.all()
    categs = session['dicc_categorias']
    hora_inicio = session['hora_inicio']
    if(session['hora_inicio'] == None):
        print("pongo hora inicio")
        session['hora_inicio'] = datetime.datetime.now()
        hi = session['hora_inicio']
        hora_inicio = hi.strftime("%d/%m/%Y - %H:%M:%S")

    print("Categorias en mostrarcategorias = ", session['dicc_categorias'])
    return render_template('categorias.html', categorias=categorias, inicio=hora_inicio)


@public_bp.route('/trivia/<int:id_categoria>/pregunta', methods=['GET'])
@login_required
def mostrarpregunta(id_categoria):
    preguntas = Pregunta.query.filter_by(categoria_id=id_categoria).all()
    # elegir pregunta aleatoria pero de la categoria adecuada
    pregunta = random.choice(preguntas)
    categ = Categoria.query.get(id_categoria)

    respuestas = Respuesta.query.filter_by(pregunta_id=pregunta.id).all()

    return render_template('preguntas.html', categoria=categ, pregunta=pregunta, respuestas=respuestas)

@public_bp.route('/trivia/<int:id_pregunta>/resultado/<int:id_respuesta>', methods=['GET'])
@login_required
def mostrarresultado(id_respuesta,id_pregunta):
    tiempo_total = 0
    minutos = 0
    segundos = 0
    tiempo_partida = ""
    hora_fin = datetime.datetime.now()
    resp = Respuesta.query.get(id_respuesta)
    preg = Pregunta.query.get(id_pregunta)
    categ = Categoria.query.get(preg.categoria_id)

    if resp.resultado == True:
        #categs = session['dicc_categorias']
        #categs[categ.descripcion] = True
        #session['dicc_categorias'] = categs
        session['dicc_categorias'][categ.descripcion] = True
        session.modified = True

    valores = session['dicc_categorias'].values()

    if False in valores:
        #Hay alguna categoría no respondida
        return render_template('resultado.html', resultado=resp.resultado, pregunta=preg, respuesta=resp)

    tiempo_total = hora_fin - session['hora_inicio']
    print("Tiempo total = ", tiempo_total)
    #print("Hora inicio =", session['hora_inicio'], " -- hora fin = ", hora_fin)
    minutos = tiempo_total.total_seconds() / 60
    segundos = tiempo_total.total_seconds() % 60

    tiempo_partida = str(int(minutos)) + " minutos y " + str(int(segundos)) + " segundos"
    #print("Cant minutos = ", minutos, " -- segundos = ", segundos)
    print("Menor tiempo del usuario conectado = ", current_user.menor_tiempo)
    if current_user.menor_tiempo == None:
        current_user.update(current_user.email, tiempo_total)
    else:
        if int(tiempo_total.total_seconds()) < int(current_user.menor_tiempo):
            current_user.update(current_user.email,tiempo_total)

    return render_template('ganador.html', tiempo=tiempo_partida, minutos=minutos)

@public_bp.route('/trivia/mejores', methods=['GET'])
@login_required
def mostrarmejores():
    lista_mejores = User.query.filter(User.menor_tiempo!=None).order_by(User.menor_tiempo).all()

    return render_template('posiciones.html', posiciones=lista_mejores[0:10:1])

@public_bp.route('/admin')
@login_required
@admin_permission.require(http_exception=403)
#Este admin_permission es el creado en apptrivia.py
def mostraradmin():
    return render_template('admin.html')