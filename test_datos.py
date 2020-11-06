#!/usr/bin/env python
# -*- coding: utf-8 -*-

from apptrivia import db
from models.models import Categoria, Pregunta, Respuesta, User


db.drop_all()
db.create_all()

# categorias
c_geogra = Categoria(descripcion="Geografía")
c_deporte = Categoria(descripcion="Deportes")
c_historia = Categoria(descripcion="Historia")
c_arte = Categoria(descripcion="Arte")

# preguntas
q_Laos = Pregunta(text="¿Cuál es la capital de Laos?",categoria=c_geogra)
q_Australia = Pregunta(text="¿Cuál es la capital de Australia?",categoria=c_geogra)
q_Armenia = Pregunta(text="¿Cuál es la población aproximada de Armenia?",categoria=c_geogra)
q_mundial = Pregunta(text="¿En qué país se jugó la Copa del Mundo de 1962?",categoria=c_deporte)
q_bascket = Pregunta(text="¿En qué año se jugó la primer Copa del Mundo de Basquetbol?",categoria=c_deporte)
q_femenino = Pregunta(text="¿Qué país fue el último campeón mundial de fulbol femenino?",categoria=c_deporte)
q_guerra = Pregunta(text="¿En qué año inició la primer guerra mundial?",categoria=c_historia)
q_indepen = Pregunta(text="¿En qué ciudad se declaró la independencia del Uruguay?",categoria=c_historia)
q_orientales = Pregunta(text="¿Donde se realizó el desembarco de los 33 orientales?",categoria=c_historia)
q_libro = Pregunta(text="¿Quíen escribió el libro Gracias por el fuego?",categoria=c_arte)
q_movimiento = Pregunta(text="¿Para qué movimiento fue clave el aporte de Claude Monet?",categoria=c_arte)
q_pelicula = Pregunta(text="¿Quíen protagonizó la última zaga de Misión Imposible?",categoria=c_arte)

r_LaosA = Respuesta(text="Kuala Lumpur",resultado=False,pregunta=q_Laos)
r_LaosB = Respuesta(text="Timbu",resultado=False,pregunta=q_Laos)
r_LaosC = Respuesta(text="Vientián",resultado=True,pregunta=q_Laos)
r_AustraliaA = Respuesta(text="Sídney",resultado=False,pregunta=q_Australia)
r_AustraliaB = Respuesta(text="Canberra",resultado=True,pregunta=q_Australia)
r_AustraliaC = Respuesta(text="Melbourne",resultado=False,pregunta=q_Australia)
r_ArmeniaA = Respuesta(text="3.001.600",resultado=True,pregunta=q_Armenia)
r_ArmeniaB = Respuesta(text="3.550.000",resultado=False,pregunta=q_Armenia)
r_ArmeniaC = Respuesta(text="3.120.000",resultado=False,pregunta=q_Armenia)
r_MundialA = Respuesta(text="España",resultado=False,pregunta=q_mundial)
r_MundialB = Respuesta(text="Chile",resultado=True,pregunta=q_mundial)
r_MundialC = Respuesta(text="Alemania",resultado=False,pregunta=q_mundial)
r_bascketA = Respuesta(text="1959",resultado=False,pregunta=q_bascket)
r_bascketB = Respuesta(text="1963",resultado=False,pregunta=q_bascket)
r_bascketC = Respuesta(text="1950",resultado=True,pregunta=q_bascket)
r_femeninoA = Respuesta(text="Estados Unidos",resultado=True,pregunta=q_femenino)
r_femeninoB = Respuesta(text="Holanda",resultado=False,pregunta=q_femenino)
r_femeninoC = Respuesta(text="Inglaterra",resultado=False,pregunta=q_femenino)
r_guerraA = Respuesta(text="1914",resultado=True,pregunta=q_guerra)
r_guerraB = Respuesta(text="1915",resultado=False,pregunta=q_guerra)
r_guerraC = Respuesta(text="1916",resultado=False,pregunta=q_guerra)
r_indepenA = Respuesta(text="Salto",resultado=False,pregunta=q_indepen)
r_indepenB = Respuesta(text="Colonia",resultado=False,pregunta=q_indepen)
r_indepenC = Respuesta(text="Florida",resultado=True,pregunta=q_indepen)
r_orientalesA = Respuesta(text="En la Playa de Pocitos, en Montevideo",resultado=False,pregunta=q_orientales)
r_orientalesB = Respuesta(text="En la Playa de la Agraciada, Soriano",resultado=True,pregunta=q_orientales)
r_orientalesC = Respuesta(text="En la Playa Mansa de Punta del Este",resultado=False,pregunta=q_orientales)
r_libroA = Respuesta(text="Mario Benedetti",resultado=True,pregunta=q_libro)
r_libroB = Respuesta(text="Eduardo Galeano",resultado=False,pregunta=q_libro)
r_libroC = Respuesta(text="Idea Vilariño",resultado=False,pregunta=q_libro)
r_movimientoA = Respuesta(text="Expresionismo",resultado=False,pregunta=q_movimiento)
r_movimientoB = Respuesta(text="Surrealismo",resultado=False,pregunta=q_movimiento)
r_movimientoC = Respuesta(text="Impresionismo",resultado=True,pregunta=q_movimiento)
r_peliculaA = Respuesta(text="Tom Cruise",resultado=True,pregunta=q_pelicula)
r_peliculaB = Respuesta(text="Liam Neeson",resultado=False,pregunta=q_pelicula)
r_peliculaC = Respuesta(text="Brad Pitt",resultado=False,pregunta=q_pelicula)

#Usuarios
q_u1 = User(name="Maria",email="maria@antel.com.uy",admin=True)
# el pass lo seteamos con el método set_password para que se guarde con hash
q_u1.set_password("Maria123")
# por defecto, el usuario no es admin
q_u2 = User(name="Juan",email="juan@antel.com.uy")
q_u2.set_password("Juan123")

db.session.add(c_geogra)
db.session.add(c_deporte)
db.session.add(c_historia)
db.session.add(c_arte)

db.session.add(q_Laos)
db.session.add(q_Armenia)
db.session.add(q_mundial)
db.session.add(q_Australia)
db.session.add(q_bascket)
db.session.add(q_femenino)
db.session.add(q_guerra)
db.session.add(q_indepen)
db.session.add(q_orientales)
db.session.add(q_libro)
db.session.add(q_movimiento)
db.session.add(q_pelicula)

db.session.add(r_LaosA)
db.session.add(r_LaosB)
db.session.add(r_LaosC)
db.session.add(r_ArmeniaA)
db.session.add(r_ArmeniaB)
db.session.add(r_ArmeniaC)
db.session.add(r_MundialA)
db.session.add(r_MundialB)
db.session.add(r_MundialC)
db.session.add(r_AustraliaA)
db.session.add(r_AustraliaB)
db.session.add(r_AustraliaC)
db.session.add(r_bascketA)
db.session.add(r_bascketB)
db.session.add(r_bascketC)
db.session.add(r_femeninoA)
db.session.add(r_femeninoB)
db.session.add(r_femeninoC)
db.session.add(r_guerraA)
db.session.add(r_guerraB)
db.session.add(r_guerraC)
db.session.add(r_indepenA)
db.session.add(r_indepenB)
db.session.add(r_indepenC)
db.session.add(r_orientalesA)
db.session.add(r_orientalesB)
db.session.add(r_orientalesC)
db.session.add(r_libroA)
db.session.add(r_libroB)
db.session.add(r_libroC)
db.session.add(r_movimientoA)
db.session.add(r_movimientoB)
db.session.add(r_movimientoC)
db.session.add(r_peliculaA)
db.session.add(r_peliculaB)
db.session.add(r_peliculaC)

db.session.add(q_u1)
db.session.add(q_u2)

db.session.commit()

# creamos otros usuarios (…) y los recorremos
categorias = Categoria.query.all()
for c in categorias:
    print(c.id, c.descripcion)
    # para cada categoria, obtenemos sus preguntas y las recorremos, c.preguntas es el preguntas que cree en la case Categoria y actualizo
    # cada vez que creo una pregunta para esa categoría
    for p in c.preguntas:
        print(p.id, p.text)


cat = Categoria.query.get(1)
print(cat)
