# Database
# from src.bd.bd import MyDbEnty
from errno import errorcode
from ..dto.dtoImage import ImagenDTO
from mysql.connector import Error
import mysql
from mysql.connector import IntegrityError
from flask import jsonify, request
# from ..bd import bd  as base
from ..bd import bdxamm as base
from decouple import config as datos
bd = base.MyDbEnty()


class uploads():

    async def loadfile(self, IMAGEN: ImagenDTO):
        try:
            connection = bd.conectar_con_bd()
            cursor = connection.cursor()
            # cursor.execute("SET GLOBAL max_allowed_packet=67108864;")
            # Ejecutar el procedimiento almacenado
            cursor.execute("Call almacenar_foto (%s, %s)",
                           (IMAGEN.namefile, IMAGEN.datafile,))

            # Capturar la salida del procedimiento almacenado
           # result = cursor.fetchone()
           # print('Varible ',result)
           # success_message = result[1] if result else None
           # print('Seccess Message',success_message)
            cursor.close()
            connection.commit()
            bd.kill_conexion(connection)

            return jsonify({"Carga De Imagen Completada": IMAGEN.namefile}), 201
        except Error as error:
            if error.errno == 1644:
                bd.kill_conexion(connection)
                return jsonify({"error": "Los datos ya existen en la base de datos"}), 400
            elif error.errno == 1305:
                return jsonify({"error": "El procedimiento almacenado no existe"}), 500
            else:
                return jsonify({"error": "Error desconocido", "informacion": str(error)}), 500

    def downloadfile(self, json):
        try:
            id = json.get('id')
            connection = bd.conectar_con_bd()
            cursor = connection.cursor()
            cursor.execute("Call obtener_foto(%s)", (id,))
            rv = cursor.fetchall()
            cursor.close()
            bd.kill_conexion(connection)

            # Verificar si se obtuvieron resultados
            if rv is not None:

                for result in rv:
                    # Suponiendo que 'namefile' es el primer elemento y 'datafile' el segundo en el resultado
                    namefile = result[0]
                    datafile = result[1]

                    return ImagenDTO(namefile, datafile), 200
                else:
                    # No se encontraron registros para el id dado
                    return {"error": "No se encontró el registro."}, 404

        except IntegrityError as error:
            return jsonify({"error": "Violación de la integridad de la clave única", "informacion": str(error)}), 500

        except Exception as error_general:
            return jsonify({"error": "Error general", "informacion": str(error_general)}), 500
