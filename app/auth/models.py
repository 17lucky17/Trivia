# importamos la instancia de la BD
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    menor_tiempo = db.Column(db.Integer, nullable=True)
    roles = db.relationship('Role', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {} - Email {}>'.format(self.name, self.email)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def update(self, email, tiempo_total):
        if self.id:
            User.query.filter_by(email=email).update(dict(menor_tiempo=int(tiempo_total.total_seconds())))
        db.session.commit()

    @staticmethod
    #User.get_by_id - eso es estatico, no necesito una instancia de la clase y por ser estático no recibe self
    def get_by_id(id):
        return User.query.get(id)

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    rolename = db.Column(db.String(60), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'<Role {self.rolename}>'