from src.dto.dtoImage import ImagenDTO
from ..models import m_uploads

modelo_upload = m_uploads.uploads()

class UploadController():
    def c_upload(self, Image: ImagenDTO):
        data= modelo_upload.loadfile(Image)
        return data
    
    def c_getfoto(self, json):
        data = modelo_upload.downloadfile(json)
        return data