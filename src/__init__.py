# Importacion De Librerias
from flask import Flask
from flask_cors import CORS
from flask_uploads import UploadSet, configure_uploads, IMAGES
import os
from decouple import config as datos

# Routes
from src.routes import route_usuario
from src.routes import route_uploads
from src.routes import route_autenticacion
from src.routes import route_autorizacion


###############
app = Flask(__name__,  template_folder='templates')


def _init_app(config):
    # Configuration
    app.config.from_object(config)
    app.config['SECRET_KEY'] = datos('SECRET_KEY')
    app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(
        os.getcwd(), 'app', 'uploads')

    photos = UploadSet('photos', IMAGES)
    configure_uploads(app, photos)
    #CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}}) ##CORS DEFAULT
    CORS(app)
    # Blueprints
    app.register_blueprint(route_uploads.uploadsFile,
                           url_prefix='/uploads')
    app.register_blueprint(
        route_usuario.Usuarios_blueprint, url_prefix='/usuarios')
    app.register_blueprint(
        route_autenticacion.autenticacion, url_prefix='/autenticacion')
    app.register_blueprint(route_autorizacion.verify_token,
                           url_prefix='/verify_token')
    return app
