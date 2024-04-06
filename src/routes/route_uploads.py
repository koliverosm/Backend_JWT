from flask import jsonify, request, Blueprint
from flask_cors import cross_origin
from flask_uploads import UploadNotAllowed
from flask_uploads import UploadSet, IMAGES
from werkzeug.utils import secure_filename
from random import sample
import os
from ..controllers import uploadscontroller
from cryptography.fernet import Fernet
import base64
from decouple import config as datos

carga = uploadscontroller.UploadController()
Carga_blueprint = Blueprint('carga', __name__)
photos = UploadSet('photos', IMAGES)


################# FUNCIONES PRINCIPALES#############################
def name_face_generator():
    # Generando string aleatorio
    string_aleatorio = "CUL0123456789"
    longitud = 10
    secuencia = string_aleatorio.upper()
    resultado_aleatorio = sample(secuencia, longitud)

    string_aleatorio = "".join(resultado_aleatorio)
    return string_aleatorio


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def __encrypt(photo_encryted: bytes):
    clave: str = datos('SECRET_KEY_PHOTO')
    print("Esta Es La Clave SECRET: " + clave)
    fernet = Fernet(clave)
    foto_encriptada = fernet.encrypt(photo_encryted)
    return foto_encriptada

###############################################


@Carga_blueprint.route('/')
@cross_origin()
def index():

    return jsonify({'message': 'Welcome Estas En Ruta Uploads, Apartir De Aqui Todo LLeva /uploads/ + La Ruta Que Deseas Acceder'})


@Carga_blueprint.route('/file', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        try:
            file = request.files['image']
            # Verificar que el archivo sea una imagen
            if file and allowed_file(file.filename):
                # La ruta donde se encuentra el archivo actual
                basepath = os.path.dirname(__file__)
                # Nombre original del archivo
                filename = secure_filename(file.filename)

                # Guardar el archivo en el sistema de archivos
                extension = os.path.splitext(filename)[1]
                nuevoNombreFile = name_face_generator() + extension
                upload_path = os.path.join(
                    basepath, '../uploads/Face_reco', nuevoNombreFile)
                file.save(upload_path)
                ##### Encriptar La Foto En Formarlo BLOB Para la base de datos #####
                with open(upload_path, 'rb') as f:
                    foto = f.read()
                 #

              #  respuesta = carga.c_upload(filename, foto)
               # print('Esta Es la Repuesta Despues De Subir', respuesta)

                # print(respuesta)
                return 'Archivo subido con éxito: {}'.format(filename)
            else:
                return 'Tipo de archivo no permitido. Por favor, suba solo archivos de imagen.'
        except UploadNotAllowed:
            return 'Tipo de archivo no permitido'
    return 'No se ha subido ningún archivo'
