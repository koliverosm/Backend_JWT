from config import *
from flask import jsonify, request
# from ..bd import bd  as base
from ..bd import bdxamm as base
bd = base.MyDbEnty()
# bd = base.MyDbEnty()


class Usuario():

    def crear_usuario(self, data):
        try:
            connection = bd.conectar_con_bd()
            username = data.get("username")
            password = data.get("password")
            print("Estoy en el controlador", username)
            cursor = connection.cursor()
            cursor.execute("CALL Insertar_usuario(%s,%s)",
                           (username, password,))
            cursor.close()
            print("Estoy despues de llamarla", username)
            connection.commit()
            return jsonify({"Se Agrego Correctamente El Usuario": username}), 201

        except Exception as error_general:
            return jsonify({"error": "Error general", "informacion": str(error_general)}), 500

    def crear_user_admin(self, data):
        try:
            connection = bd.conectar_con_bd()
            # Extraer los datos del JSON
            username = data.get("username")
            password = data.get("password")
            rol = data.get("rol")
            statu = data.get("statu")

            cursor = connection.cursor()
            cursor.execute("CALL Insertar_usuario_admin (%s,%s,%s,%s)",
                           (username, password, rol, statu))
            cursor.close()
            connection.commit()
            return jsonify({"Usuario Admnistrador Agregado Correctamente": username}), 201

        except (Exception) as error:
            return jsonify({"informacion": error}), 406

    def getDato(self):
        # id , nombre , nombre_2 , apellido , apellido_2 ,
        return {
            'id': id,
            'nombre': self.nombre,
            'nombre_2': self.nombre_2,
            'apelido': self.apelido,
            'apelido_2': self.apelido_2,
            'usuario': self.usuario,
            'password': self.password,
            'key': self.key,
            'fecha_expiracion': self.fecha_expiracion,
            'fecha_creacion': self.fecha_creacion
        }

    def m_consultar_usuarios(self):
        try:
            connection = bd.conectar_con_bd()
            cursor = connection.cursor()
            cursor.execute("Call ListarUsuarios()")
            rv = cursor.fetchall()
            cursor.close()
            payload = []
            content = {}
            bd.kill_conexion(connection)
            for result in rv:
                valor_bytearray = result[2]
                valor_cadena = valor_bytearray.decode()
                valor_final = valor_cadena[0:-1]
                content = {'id': result[0],
                           'username': result[1],
                           'password': valor_final,
                           'roles': result[3],
                           'date': result[4]}
                payload.append(content)
                content = {}
            print(result[2])
            return jsonify({"data": payload}), 200
        except (Exception) as error:
            return jsonify({"error": str(error)})

    def m_crear_usuario_postgres(self):
        try:
            connection = bd.conectar_con_bd()
            nombre = request.json['nombre']
            nombre_2 = request.json['nombre_2']
            apellido = request.json['apellido']
            apellido_2 = request.json['apellido_2']
            usuario = request.json['usuario']
            password = request.json['password']
            key = request.json['key']
            fecha_expiracion = request.json['fecha_expiracion']
            fecha_creacion = request.json['fecha_creacion']

            cursor = connection.cursor()
            cursor.execute("INSERT INTO usuarios (nombre,nombre_2,apellido,apellido_2,usuario,password,key,fecha_expiracion,fecha_creacion) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                           (nombre, nombre_2, apellido, apellido_2, usuario, password, key, fecha_expiracion, fecha_creacion))
            cursor.connection.commit()
            cursor.close()

            return jsonify({"informacion": "ok"})

        except (Exception) as error:
            return jsonify({"informacion": error})

    def m_consultar_usuario_id(self):
        try:
            connection = bd.conectar_con_bd()
            id = request.json['id']
            cursor = connection.cursor()
            cursor.execute("select * from usuarios where id= %s ", (id,))
            rv = cursor.fetchall()
            cursor.close()
            payload = []
            content = {}
            for result in rv:
                content = {'id': result[0],
                           'usuario': result[1],
                           'contrasena': result[2],
                           'nombre': result[3],
                           'apellido': result[4],
                           'identificacion': result[5],
                           'correo': result[6],
                           'telefono': result[7],
                           'perfil': result[8]
                           }
                payload.append(content)
                content = {}
            print(payload)
            return jsonify(payload)
        except (Exception) as error:
            return jsonify({"informacion": error})

    def m_actualizar_usuario(self):
        try:
            connection = bd.conectar_con_bd()
            id = request.json['idusuario']
            usuario = request.json['usuario']
            contrasena = request.json['contrasena']
            nombre = request.json['nombre']
            apellido = request.json['apellido']
            correo = request.json['correo']
            telefono = request.json['telefono']
            identificacion = request.json['identificacion']
            idperfil = request.json['idperfil']
            cursor = connection.cursor()
            cursor.execute("CALL actualizar_usuario(%s,%s,%s,%s,%s,%s,%s,%s,%s)", (id, usuario,
                           contrasena, nombre, apellido, correo, telefono, identificacion, idperfil))
            cursor.connection.commit()
            cursor.close()

            return jsonify({"informacion": "ok"})

        except (Exception) as error:
            return jsonify({"informacion": error})

    def m_bajar_usuario(self):
        try:
            connection = bd.conectar_con_bd()
            usuario = request.json['usuario']
            cursor = connection.cursor()
            cursor.execute("CALL bajar_usuario(%s)", (usuario,))
            cursor.connection.commit()
            cursor.close()

            return jsonify({"informacion": "ok"})

        except (Exception) as error:
            return jsonify({"informacion": error})
