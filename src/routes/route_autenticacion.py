
from flask_cors import cross_origin
from flask import Blueprint, request, jsonify


# Models
from src.models.m_login import User_login
# Security
from src.utils.service_cifrado import Security
# Services
from src.controllers.logincontroller import Logincontroller
from src.models.autenticacion.m_authe import AuthService

autenticacion = Blueprint('autenticacion', __name__)


@autenticacion.route('/', methods=['GET', 'POST'])
def index():
    return jsonify({'success': 'Estas En La Ruta Autenticacion'})


@cross_origin
@autenticacion.route('/generated_token', methods=['POST'])
def auten_token():
    username = request.json['username']
    password = request.json['password']
    _user = User_login(0, username, password, None)
    authenticated_user = Logincontroller.c_login(_user)

    if (authenticated_user != None):
        encoded_token = Security.generate_token(authenticated_user)
        return jsonify({'success': True, 'token': encoded_token}), 201
    else:
        return jsonify({'message': 'Unauthorized'}), 401
