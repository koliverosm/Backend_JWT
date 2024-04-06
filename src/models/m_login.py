from config import *
from flask import jsonify, request
# from ..bd import bd  as base
from ..bd import bdxamm as base
bd = base.MyDbEnty()
# bd = base.MyDbEnty()


class User_login():

    @classmethod
    def __init__(self, id, username, password,  roles) -> None:
        self.__id = id
        self.__username = username
        self.__password = password
        self.__roles = roles

    @classmethod
    def user_create(self, id, username, password, fullname, roles) -> None:
        self.__id = id
        self.__username = username
        self.__password = password
        self.__fullname = fullname
        self.__roles = roles
        print("user")

    @classmethod
    def crear_user_login(self):
        try:
            connection = bd.conectar_con_bd()
            self.set_username(request.json['username'])
            self.set_password(request.json['password'])
            self.set_fullname(request.json['fullname'])
            self.__roles = request.json['roles']
            cursor = connection.cursor()
            cursor.execute("Call sp_addUser (%s,%s,%s,%s)", (self.get_username(
            ), self.get_password(), self.get_fullname(), self.get_roles()))
            connection.commit()
            cursor.close()
            return jsonify({'message': 'Inserción exitosa'})

        except Exception as e:
            print('Error al Insertar USER: ', e)

    def get_id(self):
        return self.__id

    def set_id(self, id):
        self.__id = id

    def get_username(self):
        return self.__username

    def set_username(self, username):
        self.__username = username

    def get_password(self):
        return self.__password

    def set_password(self, password):
        self.__password = password

    def get_fullname(self):
        return self.__fullname

    def set_fullname(self, fullname):
        self.__fullname = fullname

    def get_roles(self):
        return self.__roles
