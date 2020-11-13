# importamos la instancia de Flask (app)
from . import errors_bp
from flask import render_template
from werkzeug.exceptions import HTTPException

@errors_bp.app_errorhandler(404)
def page_not_found(e):
    mensaje = "La página a la que desea acceder no existe."
    #return jsonify(error=str(e)), 404
    return render_template('error.html', mensaje=mensaje)
    #return render_template('404.html')


@errors_bp.app_errorhandler(401)
def unathorized(e):
    mensaje = "Debes estar logueado para acceder a esta funcionalidad."
    return render_template('error.html', mensaje=mensaje)

#Logueado pero no tiene permisos para el recurso al que quiere acceder
@errors_bp.app_errorhandler(403)
def unathorized(e):
    mensaje = "No tienes permiso para acceder a esta funcionalidad."
    return render_template('error.html', mensaje=mensaje)

@errors_bp.app_errorhandler(HTTPException)
def handle_exception(e):
    #return jsonify(error=str(e)), e.code
    mensaje = "Ha ocurrido un error inesperado. Intenta nuevamente más tarde."
    return render_template('error.html', mensaje=mensaje)
