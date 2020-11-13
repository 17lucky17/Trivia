#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import db
from app.auth.models import  User, Role

# agregamos 2 usuarios
u1 = User(name='administrador', email='admin@antel.com.uy',menor_tiempo=None)
u2 = User(name='Jaimito', email='bla2@antel.com.uy',menor_tiempo=None)
u1.set_password("345678")
u2.set_password("456789")
db.session.add_all([u1, u2])
db.session.commit()

u3 = User.query.filter_by(email="ldelgado@antel.com.uy").first()
u4 = User.query.filter_by(email="17lucky17@gmail.com").first()
u5 = User.query.filter_by(email="admin@app.com").first()
db.session.add_all(
         [Role(rolename='admin', user=u1),
          Role(rolename='user', user=u1),  # multiples roles
          Role(rolename='user', user=u2),
          Role(rolename='user', user=u3),
          Role(rolename='user', user=u4),
          Role(rolename='admin', user=u5)])

db.session.commit()