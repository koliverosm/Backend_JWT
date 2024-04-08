# Database
# from src.bd.bd import MyDbEnty
import mimetypes
from mysql.connector import IntegrityError
from flask import jsonify, request
# from ..bd import bd  as base
from ..bd import bdxamm as base
from decouple import config as datos
bd = base.MyDbEnty()
import io

class uploads():

    def loadfile(self, filename, file: bytes):
        try:
            connection = bd.conectar_con_bd()
            cursor = connection.cursor()
            cursor.execute("Call almacenar_foto (%s, %s)",
                           (filename, file,))
            cursor.close()
            connection.commit()
            return jsonify({"Carga De Imagen Completada": filename}), 201

        except IntegrityError as error:
            return jsonify({"error": "Violación de la integridad de la clave única", "informacion": str(error)}), 500

        except Exception as error_general:
            return jsonify({"error": "Error general", "informacion": str(error_general)}), 500

    def downloadfile(self):
        try:
            connection = bd.conectar_con_bd()
            cursor = connection.cursor()
            cursor.execute(
                "SELECT namefile , datafile FROM data_faces WHERE id = (2)")
            rv = cursor.fetchall()
            cursor.close()
            
            bd.kill_conexion(connection)

            for result in rv:
                valor_bytearray = result[1]
               
    

            return valor_bytearray, 200

            

        except IntegrityError as error:
            return jsonify({"error": "Violación de la integridad de la clave única", "informacion": str(error)}), 500

        except Exception as error_general:
            return jsonify({"error": "Error general", "informacion": str(error_general)}), 500
