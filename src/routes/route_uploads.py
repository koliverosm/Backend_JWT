import uuid as has_id_face
import asyncio
from flask import jsonify, request, Blueprint
from flask_cors import cross_origin
from flask_uploads import UploadNotAllowed, UploadSet, IMAGES
from werkzeug.utils import secure_filename
from random import sample
import os

from src import uploads
from src.dto.dtoImage import ImagenDTO
from ..controllers import uploadscontroller
from cryptography.fernet import Fernet
import base64
from decouple import config as datos

carga = uploadscontroller.UploadController()
uploadsFile = Blueprint('uploadsFile', __name__)
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
    clave: str = datos('SECRET_KEY_PHOTO')  # type: ignore
    print("Esta Es La Clave SECRET: ", clave)
    fernet = Fernet(clave)  # type: ignore
    foto_encriptada = fernet.encrypt(photo_encryted)
    return foto_encriptada

###############################################


@uploadsFile.route('/')
@cross_origin()
def index():

    return jsonify({'message': 'Welcome Estas En Ruta Uploads, Apartir De Aqui Todo LLeva /uploads/ + La Ruta Que Deseas Acceder'})


@uploadsFile.route('/getfoto', methods=['POST', 'GET'])  # type: ignore
async def getfoto():
    data = request.get_json()
    foto_info, status_code = carga.c_getfoto(data)  # type: ignore

    if foto_info and status_code == 200:
        basepath = os.path.dirname(__file__)
        # Crear el path completo incluyendo el nombre del archivo para guardar la imagen
        upload_path = os.path.join(
            basepath, '../uploads/photo_query', f'{foto_info.namefile}')
        # Escribir los bytes de la imagen en el archivo
        with open(upload_path, 'wb') as archivo:
            archivo.write(foto_info.datafile)  # type: ignore
        foto_base64 = base64.b64encode(foto_info.datafile).decode('utf-8')
        # with open(upload_path, 'rb') as f:
        #          foto = f.read()
        return jsonify({'namefile': f'{foto_info.namefile}', 'file': foto_base64, 'id_face': f'{foto_info.id_face}'}), status_code
    else:
        return jsonify({'Error': 'No se pudo obtener la foto'}), 404


@uploadsFile.route('/file', methods=['POST'])
async def upload_file():

    if request.method == 'POST':
        try:
            file = request.files['image']
            print("Esto Llega De JS ", request.files['image'])
            # Verificar que el archivo sea una imagen
            if file and allowed_file(file.filename):
                # La ruta donde se encuentra el archivo actual
                basepath = os.path.dirname(__file__)
                # Nombre original del archivo
                filename = secure_filename(file.filename)  # type: ignore

                # Guardar el archivo en el sistema de archivos
                extension = os.path.splitext(filename)[1]
                nuevoNombreFile = filename + extension  # name_face_generator() + extension
                upload_path = os.path.join(
                    basepath, '../uploads/Face_reco', nuevoNombreFile)

                file.save(upload_path)
                ##### Encriptar La Foto En Formarlo BLOB Para la base de datos #####
                with open(upload_path, 'rb') as f:
                    foto = f.read()
               # respuesta = ""
               # code = 201
                id_face = has_id_face.uuid5(
                    has_id_face.NAMESPACE_DNS, f'{filename}')
                
                respuesta, code = await carga.c_upload(ImagenDTO(filename, foto, f'{id_face}'))
                #print('Esta Es la Repuesta Despues De Subir ROUTES',respuesta, "Codigo", code)
                if code == 201:
                    # si se sube correctamente en la base de datos se guarda en el directorio
                    # file.save(upload_path)
                    return respuesta, 201
                elif code == 400:

                    return respuesta, 400
            else:
                #print("Tipo de archivo no permitido. Por favor, suba solo archivos de imagen.")
                return 'Tipo de archivo no permitido. Por favor, suba solo archivos de imagen.'
        except UploadNotAllowed:
            return 'Tipo de archivo no permitido'
    return 'No se ha subido ningún archivo'
