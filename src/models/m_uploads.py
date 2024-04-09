# Database
# from src.bd.bd import MyDbEnty
import mimetypes
from mysql.connector import IntegrityError
from flask import jsonify, request
# from ..bd import bd  as base
from ..bd import bdxamm as base
from decouple import config as datos
bd = base.MyDbEnty()
from ..dto.dtoImage import ImagenDTO

class uploads():

    def loadfile(self, IMAGEN:ImagenDTO):
        try:
            connection = bd.conectar_con_bd()
            cursor = connection.cursor()
            cursor.execute("Call almacenar_foto (%s, %s)",
                           (IMAGEN.namefile, IMAGEN.datafile,))
            cursor.close()
            connection.commit()
            return jsonify({"Carga De Imagen Completada": IMAGEN.namefile}), 201

        except IntegrityError as error:
            return jsonify({"error": "Violación de la integridad de la clave única", "informacion": str(error)}), 500

        except Exception as error_general:
            return jsonify({"error": "Error general", "informacion": str(error_general)}), 500

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
                        
                        return ImagenDTO(namefile, datafile),200
                else:
                    # No se encontraron registros para el id dado
                    return {"error": "No se encontró el registro."}, 404
                
        except IntegrityError as error:
                  return jsonify({"error": "Violación de la integridad de la clave única", "informacion": str(error)}), 500

        except Exception as error_general:
                return jsonify({"error": "Error general", "informacion": str(error_general)}), 500
