from ..models.autenticacion.m_authe import AuthService 
mod_login = AuthService()

class Logincontroller():
    
    @classmethod
    def c_login(self, users):
        data= mod_login.login_user(users)
        return data