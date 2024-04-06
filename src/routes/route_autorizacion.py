from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
# Errors
from ..utils.service_error import CustomException
# Security
from src.utils.service_cifrado import Security
verify_token = Blueprint('verify_token', __name__)


@verify_token.route('/', methods=['GET', 'POST'])
def index():
    return jsonify({'success': 'Estas En La Ruta verify_token '}), 200


@verify_token.route('/up', methods=['GET', 'POST'])
@cross_origin()
def verifytoken():
    try:
        print('Estos Son Lo Headers: ', request.headers)
        autorizacion, has_access = Security.verify_token(request.headers)
        print('La Validacion Es: ', has_access)

        if autorizacion:
            response = jsonify({'message': autorizacion, 'data': has_access})
            return response, 200

        else:
            if has_access == 'token invalid':

                return jsonify({"error": has_access, 'message': False}), 403
            if has_access == 'token expired':
                return jsonify({"error": has_access, 'message': False}), 203
            else:
                return jsonify({'message': 'Unauthorized'}), 401

    except CustomException as ce:
        return jsonify({'message': str(ce), 'success': False}), 404
    except Exception as e:
        return jsonify({'message': str(e), 'success': False}), 503
