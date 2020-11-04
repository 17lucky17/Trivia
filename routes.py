# importamos la instancia de Flask (app)
from apptrivia import app
import random
import datetime
import os
# importamos los modelos a usar
from models.models import Categoria, Pregunta, Respuesta

from flask import render_template, session, redirect, url_for

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or \
    'e5ac358c-f0bf-11e5-9e39-d3b532c10a28'

#con esta puedo probar si llego hasta acá -  http://localhost:5000/trivia
@app.route('/trivia')
def index():
    print(" &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& INDEX")
    session.clear()
    dicc_categorias = {"Geografía":False, "Deportes":False,"Historia":False,"Arte":False}
    session['hora_inicio'] = datetime.datetime.now()
    session['dicc_categorias'] = dicc_categorias

    """
    session['dicc_categorias']["Arte"] = True
    print("Valores diccionario = ", dicc_categorias.values())
    print("Valores session = ", session['dicc_categorias'].values())
    valores = []
    valores = session['dicc_categorias'].values()
    #print("Valores = ", valores)  # puedo ver si existe un valor en la lista?
    if True in valores:
        print("Hay trues")
    else:
        print("NO hay trues")
    print("Cats= ", session['dicc_categorias'])
    """

    return redirect(url_for('mostrarcategorias'))



@app.route('/trivia/categorias', methods=['GET'])
def mostrarcategorias():
    categorias = Categoria.query.all()
    categs = session['dicc_categorias']
    hi = session['hora_inicio']
    hora_inicio = hi.strftime("%d/%m/%Y - %H:%M:%S")
    print("Categorias en mostrarcategorias = ", session['dicc_categorias'])
    return render_template('categorias.html', categorias=categorias, inicio=hora_inicio)


@app.route('/trivia/<int:id_categoria>/pregunta', methods=['GET'])
def mostrarpregunta(id_categoria):
    preguntas = Pregunta.query.filter_by(categoria_id=id_categoria).all()
    # elegir pregunta aleatoria pero de la categoria adecuada
    pregunta = random.choice(preguntas)
    categ = Categoria.query.get(id_categoria)

    respuestas = Respuesta.query.filter_by(pregunta_id=pregunta.id).all()

    return render_template('preguntas.html', categoria=categ, pregunta=pregunta, respuestas=respuestas)

@app.route('/trivia/<int:id_pregunta>/resultado/<int:id_respuesta>', methods=['GET'])
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
        categs = session['dicc_categorias']
        print("Categoria que cambio = ", categ.descripcion)
        categs[categ.descripcion] = True
        session['dicc_categorias'] = categs
        #session['dicc_categorias'][categ.descripcion] = True
        #session.modified = True

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