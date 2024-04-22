from flask import jsonify ,Blueprint , request 

voice = Blueprint('voice', __name__)


@voice.route('/' , methods=['GET'])
def index():
    return jsonify({'message': 'Welcome Estas En Ruta Voice, Apartir De Aqui Todo LLeva /voice/+La Ruta Que Deseas Acceder'})

@voice.route('/voice' , methods=['GET', 'POST'])
def voice():

    return jsonify({ 'response' : ''})
