# Database
#from src.bd.bd import MyDbEnty
from ...bd.bdxamm import MyDbEnty
# Errors
from ...utils.service_error import CustomException
# Models
from ..m_login import User_login


bd = MyDbEnty()


class AuthService():

    
    def login_user(cls, user):
        try:
            connection = bd.conectar_con_bd()
            authenticated_user = None
            with connection.cursor() as cursor:
                cursor.execute('call Validar_identidad(%s, %s)', (user.get_username(),user.get_password()))
                row = cursor.fetchone()
                if row != None:
                    bd.kill_conexion(connection)
                    print('ID: ',row[0],' USERNAME: ', row[1],'CONTRASEÑA: ', None, 'ROL: ', row[2]) 
                    authenticated_user = User_login(int(row[0]), row[1], None, row[2])
            return authenticated_user
        except CustomException as ex:
            print( CustomException(ex))