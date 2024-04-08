from ..models import m_uploads

modelo_upload = m_uploads.uploads()

class UploadController():
    def c_upload(self, filename, file:bytes):
        data= modelo_upload.loadfile(filename , file)
        return data
    
    def c_getfoto(self ):
        data = modelo_upload.downloadfile()
        return data