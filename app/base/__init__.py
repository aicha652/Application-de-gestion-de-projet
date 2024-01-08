# -*- encoding: utf-8 -*-

from flask import Blueprint


blueprint = Blueprint(
    'base_blueprint',
    __name__,
    url_prefix='',
    template_folder='templates',
    static_folder='static'
)

from app import api
from .auth import Auth, PasswordForget

api.add_resource(Auth, '/api/auth/login')
# registration route not used
# api.add_resource(Register, '/api/auth/register')

api.add_resource(PasswordForget, '/api/auth/forgot')


