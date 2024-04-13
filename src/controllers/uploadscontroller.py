from src.dto.dtoImage import ImagenDTO
from src.models.m_client import UserFile
from ..models import m_uploads

modelo_upload = m_uploads.uploads()


class UploadController():

    
    async def c_upload_userFile(self, UserFile: UserFile, File: ImagenDTO):
        data = modelo_upload.load_userFile_form(UserFile, File)
        return data

    async def c_upload(self, Image: ImagenDTO):
        data =  await modelo_upload.loadfile(Image)
        return data

    def c_getfoto(self, json):
        data = modelo_upload.downloadfile(json)
        return data
