import os

# configuraciones. True para que el servidor pueda ser levantado en modo debug
DEBUG = True

# configuracion BD

POSTGRES = {
'user': 'postgres',
    'pw': 'primavera',
    'db': 'Trivia',
    'host': '127.0.0.1',
    'port': '5432',
}
"""
    'user': 'postgres',
    'pw': 'postgres',
    'db': 'Trivia',
    'host': '172.17.0.2',
    'port': '5432',
    """

SECRET_KEY =  'A SECRET KEY'
#SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

SQLALCHEMY_TRACK_MODIFICATIONS = False

#postgresql://username:password@hostname/database
#SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5432/trivia"

SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES['user']}:" \
                          f"{POSTGRES['pw']}@{POSTGRES['host']}:" \
                          f"{POSTGRES['port']}/{POSTGRES['db']}"

