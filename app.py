######### Importaciones Para El Uso De Backend MVC########
from flask import jsonify
from config import config
from decouple import config as datos
from src import init_app
from datetime import datetime, timedelta

################# END###################################
## INICIALIZADOR DEL BACKEND LLAMANDO LA CLASE INIT_APP##
configuracion = (config['development'])
app = init_app(configuracion)

# cors = CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}})
# CORS(app)
################# END###################################


@app.route('/')
def index():
    name = 'Backend Desarrollado En Python'
    teams = 'Kevin Oliveros - Isaac Perez - Roberto Linero '
    date = datetime.now()
    date = date - timedelta(days=30 + 2)
    print(date)
    return jsonify({'Development:': name, 'Teams: ': teams, 'Fecha De Inicio': date}), 200

############### END##################################
# SALIDA PRINCIPAL AL ERROR DE RUTAS NO ECNONTRADAS#


def pagina_no_encontrada(error):
    return "<h1>Señor Usuario La Pagina A Donde Intenta Acceder No Existe...</h1>", 404
##################### END################################


if __name__ == "__main__":
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(host=datos('HOST'), port=datos('PORT'))  # type: ignore
